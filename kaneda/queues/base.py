

class BaseQueue(object):
    """
    Base class for queues

    settings_namespace is a class attribute that will be used to get the needed
    parameters to create new queue instance from a settings file.
    """
    settings_namespace = None

    def report(self, name, metric, value, tags, id_):
        raise NotImplemented()
