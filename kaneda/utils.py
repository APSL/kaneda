from __future__ import absolute_import

import os
from importlib import import_module
from six import string_types

from kaneda.exceptions import SettingsError, UnexistingKanedaClass

DEFAULT_SETTINGS_ENVAR = 'KANEDA_SETTINGS_MODULE'
DEFAULT_SETTINGS_MODULE = 'kanedasettings'


def import_class(path_or_callable):
    if hasattr(path_or_callable, '__call__'):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, string_types)
        package, attr = path_or_callable.rsplit('.', 1)
        return getattr(import_module(package), attr)


def get_settings():
    """
    Get settings from DEFAULT_SETTINGS_MODULE file or from the previously defined
    DEFAULT_SETTINGS_ENVAR environment variable pointing to the desired settings filename.
    """
    settings_module = os.environ.get(DEFAULT_SETTINGS_ENVAR, DEFAULT_SETTINGS_MODULE)
    return import_module(settings_module)


def get_object_from_settings(class_path, settings):
    """
    Get a backend/queue object from a settings file. It will convert all the
    settings definition in order to can be passed as a param dict to
    the given backend specified by settings.BACKEND or settings.QUEUE.

    e.g.:
    If your backend has the attribute variable "settings_namespace" set to "MY_BACKEND" and
    your setting file has the variables MY_BACKEND_HOST and MY_BACKEND_PORT
    it will cleanup and create a dict with keys "host" and "port" as a backend parameters.
    """
    try:
        kaneda_class = import_class(class_path)
        namespace = kaneda_class.settings_namespace + '_'
        params = {k.replace(namespace, '').lower(): v for k, v in settings.__dict__.items() if k.startswith(namespace)}
        return kaneda_class(**params)
    except (ImportError, AttributeError):
        raise UnexistingKanedaClass('The selected BACKEND or QUEUE class does not exists.')


def get_backend():
    """
    Wraps the backend retrieval function in order to control if setting file is
    defined and if the defined settings are correct.
    """
    try:
        settings = get_settings()
        if not hasattr(settings, 'BACKEND'):
            raise SettingsError('You need to set BACKEND in Kaneda settings file to import a backend instance.')
        return get_object_from_settings(settings.BACKEND, settings)
    except ImportError:
        raise SettingsError('Define backend settings on {}.py or set "{}" enviroment variable '
                            'with your settings module.'.format(DEFAULT_SETTINGS_MODULE, DEFAULT_SETTINGS_ENVAR))


def get_kaneda_objects():
    """
    Returns a backend object or a queue object.
    """
    try:
        settings = get_settings()
        if hasattr(settings, 'BACKEND'):
            return get_object_from_settings(settings.BACKEND, settings), None
        if hasattr(settings, 'QUEUE'):
            return None, get_object_from_settings(settings.QUEUE, settings)
        else:
            raise SettingsError('You need to set BACKEND or QUEUE to use Kaneda with a settings file.')
    except ImportError:
        raise SettingsError('Define backend or queue settings on {}.py or set "{}" enviroment variable '
                            'with your settings module.'.format(DEFAULT_SETTINGS_MODULE, DEFAULT_SETTINGS_ENVAR))
