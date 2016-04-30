from datetime import datetime

import pytest
from elasticsearch import Elasticsearch
from pymongo import MongoClient
import rethinkdb as r
from influxdb import InfluxDBClient

from kaneda.backends import ElasticsearchBackend, LoggerBackend, MongoBackend, RethinkBackend, InfluxBackend
from kaneda.queues import CeleryQueue, RQQueue, ZMQQueue


@pytest.fixture
def elasticsearch_backend(elastic_settings):
    return ElasticsearchBackend(index_name=elastic_settings.ELASTIC_INDEX_NAME,
                                app_name=elastic_settings.ELASTIC_APP_NAME, host=elastic_settings.ELASTIC_HOST,
                                port=elastic_settings.ELASTIC_PORT, user=elastic_settings.ELASTIC_USER,
                                password=elastic_settings.ELASTIC_PASSWORD, timeout=elastic_settings.ELASTIC_TIMEOUT)


@pytest.fixture
def elasticsearch_backend_client(elastic_settings):
    client = Elasticsearch([elastic_settings.ELASTIC_HOST], port=elastic_settings.ELASTIC_PORT,
                           http_auth=(elastic_settings.ELASTIC_USER, elastic_settings.ELASTIC_PASSWORD),
                           timeout=elastic_settings.ELASTIC_TIMEOUT)
    return ElasticsearchBackend(index_name=elastic_settings.ELASTIC_INDEX_NAME,
                                app_name=elastic_settings.ELASTIC_APP_NAME, client=client)


@pytest.fixture
def elasticsearch_backend_url(elastic_settings):
    return ElasticsearchBackend(index_name=elastic_settings.ELASTIC_INDEX_NAME,
                                app_name=elastic_settings.ELASTIC_APP_NAME,
                                connection_url=elastic_settings.ELASTIC_CONNECTION_URL)


def elasticsearch_clients():
    from tests.conftest import elastic_settings
    return [elasticsearch_backend(elastic_settings()).client, elasticsearch_backend_client(elastic_settings()).client,
            elasticsearch_backend_url(elastic_settings()).client]


@pytest.fixture
def mongo_backend(mongo_settings):
    return MongoBackend(db_name=mongo_settings.MONGO_DB_NAME, collection_name=mongo_settings.MONGO_COLLECTION_NAME,
                        host=mongo_settings.MONGO_HOST, port=mongo_settings.MONGO_PORT)


@pytest.fixture
def mongo_backend_client(mongo_settings):
    client = MongoClient(host=mongo_settings.MONGO_HOST, port=mongo_settings.MONGO_PORT,
                         serverSelectionTimeoutMS=mongo_settings.MONGO_TIMEOUT)
    return MongoBackend(db_name=mongo_settings.MONGO_DB_NAME, collection_name=mongo_settings.MONGO_COLLECTION_NAME,
                        client=client)


@pytest.fixture
def mongo_backend_url(mongo_settings):
    return MongoBackend(db_name=mongo_settings.MONGO_DB_NAME, collection_name=mongo_settings.MONGO_COLLECTION_NAME,
                        connection_url=mongo_settings.MONGO_CONNECTION_URL)


def mongo_clients():
    from tests.conftest import mongo_settings
    return [mongo_backend(mongo_settings()).client, mongo_backend_client(mongo_settings()).client,
            mongo_backend_url(mongo_settings()).client]


@pytest.fixture
def rethink_backend(rethink_settings):
    return RethinkBackend(db=rethink_settings.RETHINK_DB, host=rethink_settings.RETHINK_HOST,
                          port=rethink_settings.RETHINK_PORT, timeout=rethink_settings.RETHINK_TIMEOUT)


@pytest.fixture
def rethink_backend_connection(rethink_settings):
    connection = r.connect(host=rethink_settings.RETHINK_HOST, port=rethink_settings.RETHINK_PORT,
                           db=rethink_settings.RETHINK_DB, timeout=rethink_settings.RETHINK_TIMEOUT)
    return RethinkBackend(db=rethink_settings.RETHINK_DB, connection=connection)


def rethink_clients():
    from tests.conftest import rethink_settings
    return [rethink_backend(rethink_settings()).connection, rethink_backend_connection(rethink_settings()).connection]


@pytest.fixture
def influx_backend(influx_settings):
    return InfluxBackend(database=influx_settings.INFLUX_DATABASE, host=influx_settings.INFLUX_HOST,
                         port=influx_settings.INFLUX_PORT, username=influx_settings.INFLUX_USERNAME,
                         password=influx_settings.INFLUX_PASSWORD)


@pytest.fixture
def influx_backend_client(influx_settings):
    client = InfluxDBClient(host=influx_settings.INFLUX_HOST, port=influx_settings.INFLUX_PORT,
                            username=influx_settings.INFLUX_USERNAME, password=influx_settings.INFLUX_PASSWORD,
                            database=influx_settings.INFLUX_DATABASE)
    return InfluxBackend(database=influx_settings.INFLUX_DATABASE, client=client)


@pytest.fixture
def influx_backend_url(influx_settings):
    return InfluxBackend(database=influx_settings.INFLUX_DATABASE, connection_url=influx_settings.INFLUX_CONNECTION_URL)


def influx_clients():
    from tests.conftest import influx_settings
    return [influx_backend(influx_settings()).client, influx_backend_client(influx_settings()).client,
            influx_backend_url(influx_settings()).client]


@pytest.fixture
def logger_filename():
    return '/tmp/kaneda-{}.log'.format(datetime.utcnow().strftime('%Y%m%d'))


@pytest.fixture
def logger_backend(logger_filename):
    return LoggerBackend(filename=logger_filename)


@pytest.fixture
def celery_queue(celery_settings):
    return CeleryQueue(broker=celery_settings.CELERY_BROKER)


@pytest.fixture
def rq_queue(rq_settings):
    return RQQueue(redis_url=rq_settings.RQ_REDIS_URL)


@pytest.fixture
def zmq_queue(zmq_settings):
    return ZMQQueue(connection_url=zmq_settings.ZMQ_CONNECTION_URL)
