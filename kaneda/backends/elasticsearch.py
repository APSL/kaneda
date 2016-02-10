from __future__ import absolute_import

from datetime import datetime

try:
    from elasticsearch import Elasticsearch
except ImportError:
    Elasticsearch = None

from kaneda.exceptions import ImproperlyConfigured

from .base import BaseBackend


class ElasticsearchBackend(BaseBackend):
    """
    Elasticsearch backend.

    :param index_name: name of the Elasticsearch index used to store metrics data. Default name format will be app_name-YYYY.MM.DD.
    :param app_name: name of the app/project where metrics are used.
    :param host: server host.
    :param port: server port.
    :param username: http auth username.
    :param password: http auth password.
    """
    def __init__(self, index_name, app_name, host, port, username, password):
        if not Elasticsearch:
            raise ImproperlyConfigured('You need to install the elasticsearch library to use the Elasticsearch backend.')
        self.client = Elasticsearch([{"host": host, "port": port, 'http_auth': '{}:{}'.format(username, password)}])
        self.index_name = index_name
        self.app_name = app_name

    def _get_payload(self, name, value):
        payload = super(ElasticsearchBackend, self)._get_payload(name, value)
        payload['app_name'] = self.app_name
        payload['@timestamp'] = datetime.utcnow()
        return payload

    def _get_index_name(self):
        return '{}-{}'.format(self.index_name, datetime.utcnow().strftime('%Y.%m.%d'))

    def report(self, name, metric, value, _id):
        self.client.index(index=self._get_index_name(), doc_type=metric, id=_id, body=self._get_payload(name, value))
