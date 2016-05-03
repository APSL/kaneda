from __future__ import absolute_import

import logging

from .base import BaseBackend


class LoggerBackend(BaseBackend):
    """
    Logger backend.

    :param logger: logging instance.
    :param filename: name of the file where logger will store the metrics.
    """

    def __init__(self, logger=None, filename=''):
        if logger:
            self.logger = logger
        else:
            if filename:
                handler = logging.FileHandler(filename)
            else:
                handler = logging.StreamHandler()
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _get_payload(self, name, value, metric, tags, id_):
        payload = super(LoggerBackend, self)._get_payload(name, value, tags)
        payload['metric'] = metric
        if id_:
            payload['_id'] = id_
        return payload

    def report(self, name, metric, value, tags, id_):
        payload = self._get_payload(name, value, metric, tags, id_)
        return self.logger.info(payload)
