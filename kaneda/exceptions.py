# -*- coding: utf-8 -*-

__all__ = ['ImproperlyConfigured']


class ImproperlyConfigured(ImportError):
    """
    Kaneda is improperly configured.
    """


class UnexistingBackendClass(ImportError):
    """
    Kaneda is configured with an unexisting backend
    """