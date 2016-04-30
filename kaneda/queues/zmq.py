from __future__ import absolute_import

import logging

try:
    import zmq
except ImportError:
    zmq = None

from kaneda.exceptions import ImproperlyConfigured

from .base import BaseQueue


class ZMQQueue(BaseQueue):
    """
    ZeroMQ queue

    :param connection_url: ZMQ connection url (tcp://127.0.0.1:5555).
    :param timeout: ZMQ socket timeout (milliseconds).
    """
    settings_namespace = 'ZMQ'

    def __init__(self, connection_url, timeout=300):
        if not zmq:
            raise ImproperlyConfigured('You need to install pyzmq to use the ZMQ queue.')
        context = zmq.Context()
        self.socket = context.socket(zmq.PUSH)
        self.socket.SNDTIMEO = timeout
        self.socket.bind(connection_url)

    def report(self, name, metric, value, tags, id_):
        payload = locals()
        del payload['self']
        try:
            return self.socket.send_json(payload)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
