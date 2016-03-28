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
    :param client: client instance of Elasticsearch class.
    :param connection_url: Elasticsearch connection url (https://user:secret@localhost:9200).
    :param host: server host.
    :param port: server port.
    :param username: http auth username.
    :param password: http auth password.
    :param timeout: Elasticsearch connection timeout (seconds).
    """

    def __init__(self, index_name, app_name, client=None, connection_url=None, host=None, port=None,
                 username=None, password=None, timeout=0.3):
        if not Elasticsearch:
            raise ImproperlyConfigured(
                'You need to install the elasticsearch library to use the Elasticsearch backend.')
        if client:
            if not isinstance(client, Elasticsearch):
                raise ImproperlyConfigured('"client" parameter is not an instance of Elasticsearch client')
            self.client = client
        elif connection_url:
            self.client = Elasticsearch([connection_url], timeout=timeout)
        else:
            self.client = Elasticsearch([host], port=port, http_auth=(username, password), timeout=timeout)
        self.index_name = index_name
        self.app_name = app_name

    def _get_payload(self, name, value, tags):
        payload = super(ElasticsearchBackend, self)._get_payload(name, value, tags)
        payload['app_name'] = self.app_name
        payload['@timestamp'] = datetime.utcnow()
        return payload

    def _get_index_name(self):
        return '{}-{}'.format(self.index_name, datetime.utcnow().strftime('%Y.%m.%d'))

    def report(self, name, metric, value, tags, id_):
        payload = self._get_payload(name, value, tags)
        self.client.index(index=self._get_index_name(), doc_type=metric, id=id_, body=payload)

