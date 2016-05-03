__all__ = ['ImproperlyConfigured', 'UnexistingKanedaClass', 'SettingsError']


class ImproperlyConfigured(ImportError):
    """
    Kaneda is improperly configured.
    """


class UnexistingKanedaClass(ImportError):
    """
    Kaneda is configured with an unexisting backend/queue class.
    """


class SettingsError(Exception):
    """
    Kaneda is configured without a settings file or needs a required settings variable.
    """
