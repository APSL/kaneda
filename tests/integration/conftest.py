from datetime import datetime

import pytest
from elasticsearch import Elasticsearch
from pymongo import MongoClient

from kaneda.backends import ElasticsearchBackend, LoggerBackend, MongoBackend


@pytest.fixture
def elasticsearch_backend():
    return ElasticsearchBackend(index_name='kaneda', app_name='testing', host='localhost', port=9200,
                                username='test', password='test')


@pytest.fixture
def elasticsearch_backend_client():
    client = Elasticsearch(['localhost'], port=9200, http_auth=('test', 'test'), timeout=0.3)
    return ElasticsearchBackend(index_name='kaneda', app_name='testing', client=client)


@pytest.fixture
def elasticsearch_backend_url():
    return ElasticsearchBackend(index_name='kaneda', app_name='testing',
                                connection_url='http://test:test@localhost:9200')


def elasticsearch_clients():
    return [elasticsearch_backend().client, elasticsearch_backend_client().client, elasticsearch_backend_url().client]


@pytest.fixture
def mongo_backend():
    return MongoBackend(db_name='test', collection_name='test', host='localhost', port=27017)


@pytest.fixture
def mongo_backend_client():
    client = MongoClient(host='localhost', port=27017, serverSelectionTimeoutMS=300)
    return MongoBackend(db_name='test', collection_name='test', client=client)


@pytest.fixture
def mongo_backend_url():
    return MongoBackend(db_name='test', collection_name='test', connection_url='mongodb://localhost:27017')


def mongo_clients():
    return [mongo_backend().client, mongo_backend_client().client, mongo_backend_url().client]


@pytest.fixture
def logger_filename():
    return '/tmp/kaneda-{}.log'.format(datetime.utcnow().strftime('%Y%m%d'))


@pytest.fixture
def logger_backend(logger_filename):
    return LoggerBackend(filename=logger_filename)
