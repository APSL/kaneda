import socket


class BaseBackend(object):
    """
    Base class for backend reporting storage.

    settings_namespace is a class attribute that will be used to get the needed
    parameters to create new backend instance from a settings file.
    """
    settings_namespace = None

    def report(self, name, metric, value, tags, id_):
        raise NotImplemented()

    def _get_host_name(self):
        return socket.gethostname()

    def _get_payload(self, name, value, tags):
        payload = {'host': self._get_host_name(), 'name': name}
        if isinstance(value, dict):
            payload.update(value)
        else:
            payload['value'] = value
        if tags:
            payload['tags'] = tags
        return payload
