import pytest


@pytest.fixture
def django_settings_backend(elastic_settings):
    elastic_settings.DEBUG = False
    elastic_settings.QUEUE = None
    return elastic_settings


@pytest.fixture
def django_settings_debug():
    class Settings:
        DEBUG = True
        LOGGER = None
        LOGGER_FILENAME = None

    return Settings


@pytest.fixture
def django_settings_queue(celery_settings):
    celery_settings.DEBUG = False
    celery_settings.BACKEND = None
    return celery_settings


def pytest_configure():
    from django.conf import settings
    settings.configure()
