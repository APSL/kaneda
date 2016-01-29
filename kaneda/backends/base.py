# -*- coding: utf-8 -*-
import socket


class BaseBackend(object):
    """
    Base backend
    """
    def report(self, name, metric, value, _id):
        raise NotImplemented()

    def _get_payload(self, name, value):
        return {'host': socket.gethostname(), 'name': name, 'value': value}

