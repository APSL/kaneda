import logging

from django.utils.functional import LazyObject


class LazyMetrics(LazyObject):

    def _setup(self):
        from kaneda import Metrics
        from kaneda.utils import import_class, get_object_from_settings
        from kaneda.exceptions import UnexistingKanedaClass, SettingsError
        from . import settings

        if settings.DEBUG:
            backend_class = import_class('kaneda.backends.LoggerBackend')
            if settings.LOGGER:
                backend = backend_class(logger=logging.getLogger(settings.LOGGER))
            elif settings.LOGGER_FILENAME:
                backend = backend_class(filename=settings.LOGGER_FILENAME)
            else:
                backend = backend_class()
            _metrics = Metrics(backend=backend)
        else:
            if not settings.BACKEND and not settings.QUEUE:
                raise SettingsError('You need to set KANEDA_BACKEND or KANEDA_QUEUE on settings.py to django_kaneda')
            if settings.BACKEND:
                try:
                    backend = get_object_from_settings(settings.BACKEND, settings)
                    _metrics = Metrics(backend=backend)
                except UnexistingKanedaClass:
                    raise UnexistingKanedaClass('The selected KANEDA_BACKEND class does not exists.')
            if settings.QUEUE:
                try:
                    queue = get_object_from_settings(settings.QUEUE, settings)
                    _metrics = Metrics(queue=queue)
                except UnexistingKanedaClass:
                    raise UnexistingKanedaClass('The selected KANEDA_QUEUE class does not exists.')
        self._wrapped = _metrics

metrics = LazyMetrics()
