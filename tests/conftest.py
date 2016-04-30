import pytest


class KanedaSettings:
    """
    Backend and queues settings for Kaneda.
    """
    class elastic:
        BACKEND = 'kaneda.backends.ElasticsearchBackend'
        ELASTIC_INDEX_NAME = 'test'
        ELASTIC_APP_NAME = 'test'
        ELASTIC_CONNECTION_URL = 'http://test:test@localhost:9200'
        ELASTIC_HOST = 'localhost'
        ELASTIC_PORT = 9200
        ELASTIC_USER = 'test'
        ELASTIC_PASSWORD = 'test'
        ELASTIC_TIMEOUT = 10

    class mongo:
        BACKEND = 'kaneda.backends.MongoBackend'
        MONGO_DB_NAME = 'test'
        MONGO_COLLECTION_NAME = 'test'
        MONGO_CONNECTION_URL = 'mongodb://localhost:27017'
        MONGO_HOST = 'localhost'
        MONGO_PORT = 27017
        MONGO_TIMEOUT = 300

    class rethink:
        BACKEND = 'kaneda.backends.RethinkBackend'
        RETHINK_DB = 'kaneda_test'
        RETHINK_HOST = 'localhost'
        RETHINK_PORT = 28015
        RETHINK_TIMEOUT = 0.3

    class influx:
        BACKEND = 'kaneda.backends.InfluxBackend'
        INFLUX_DATABASE = 'test'
        INFLUX_CONNECTION_URL = 'influxdb://root:root@localhost:8086/test'
        INFLUX_HOST = 'localhost'
        INFLUX_PORT = 8086
        INFLUX_USERNAME = 'root'
        INFLUX_PASSWORD = 'root'
        INFLUX_TIMEOUT = 300

    class rq:
        QUEUE = 'kaneda.queues.RQQueue'
        RQ_REDIS_URL = 'redis://localhost:6379/1'
        RQ_QUEUE_NAME = ''

    class celery:
        QUEUE = 'kaneda.queues.CeleryQueue'
        CELERY_BROKER = 'redis://localhost:6379/1'
        CELERY_QUEUE_NAME = ''

    class zmq:
        QUEUE = 'kaneda.queues.ZMQQueue'
        ZMQ_CONNECTION_URL = 'tcp://127.0.0.1:5555'
        ZMQ_TIMEOUT = 300


@pytest.fixture
def kaneda_settings():
    return KanedaSettings


@pytest.fixture
def elastic_settings():
    return KanedaSettings.elastic


@pytest.fixture
def mongo_settings():
    return KanedaSettings.mongo


@pytest.fixture
def rethink_settings():
    return KanedaSettings.rethink


@pytest.fixture
def influx_settings():
    return KanedaSettings.influx


@pytest.fixture
def celery_settings():
    return KanedaSettings.celery


@pytest.fixture
def rq_settings():
    return KanedaSettings.rq


@pytest.fixture
def zmq_settings():
    return KanedaSettings.zmq


def pytest_addoption(parser):
    parser.addoption("--run-benchmark", action="store_true", help="run benchmark tests")
