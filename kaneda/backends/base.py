# -*- coding: utf-8 -*-
import socket


class BaseBackend(object):
    """
    Base backend
    """
    def report(self, name, metric, value, tags, id_):
        raise NotImplemented()

    def _get_payload(self, name, value, tags):
        payload = {'host': socket.gethostname(), 'name': name}
        if isinstance(value, dict):
            payload.update(value)
        else:
            payload['value'] = value
        if tags:
            payload['tags'] = tags
        return payload

