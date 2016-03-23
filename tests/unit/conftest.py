import pytest

from kaneda.backends import BaseBackend


class DummyBackend(BaseBackend):
    reported_data = {}

    def report(self, name, metric, value, tags, id_=None):
        payload = self._get_payload(name, value, tags)
        payload['metric'] = metric
        self.reported_data[name] = payload


@pytest.fixture(scope='module')
def dummy_backend():
    return DummyBackend()


@pytest.fixture(scope='module')
def elasticsearch_backend_settings():
    class Settings:
        BACKEND = 'kaneda.backends.ElasticsearchBackend'
        ELASTIC_INDEX_NAME = 'test'
        ELASTIC_APP_NAME = 'test'
        ELASTIC_HOST = 'localhost'
        ELASTIC_PORT = 9200
        ELASTIC_USER = 'test'
        ELASTIC_PASSWORD = 'test'
        ELASTIC_TIMEOUT = 0.3

    return Settings


@pytest.fixture(scope='module')
def mongo_backend_settings():
    class Settings:
        BACKEND = 'kaneda.backends.MongoBackend'
        MONGO_DB_NAME = 'test'
        MONGO_COLLECTION_NAME = 'test'
        MONGO_HOST = 'localhost'
        MONGO_PORT = 27017
        MONGO_TIMEOUT = 300

    return Settings


@pytest.fixture(scope='module')
def rq_queue_settings():
    class Settings:
        QUEUE = 'kaneda.queues.RQQueue'
        RQ_REDIS_URL = 'redis://localhost:6379/1'
        RQ_QUEUE_NAME = ''

    return Settings


@pytest.fixture(scope='module')
def celery_queue_settings():
    class Settings:
        QUEUE = 'kaneda.queues.CeleryQueue'
        CELERY_BROKER = 'redis://localhost:6379/1'
        CELERY_QUEUE_NAME = ''

    return Settings


@pytest.fixture(scope='module')
def empty_settings():
    class Settings:
        pass

    return Settings


@pytest.fixture(scope='module')
def unexisting_backend_settings():
    class Settings:
        BACKEND = 'kaneda.backends.UnexsitingBackend'

    return Settings
