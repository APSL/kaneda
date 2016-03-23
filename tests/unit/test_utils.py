import pytest

from kaneda.exceptions import SettingsError, UnexistingKanedaClass
from kaneda.queues import RQQueue, CeleryQueue
from kaneda.utils import import_class, get_object_from_settings, get_kaneda_objects, get_backend
from kaneda.backends import ElasticsearchBackend, MongoBackend, LoggerBackend

from .conftest import elasticsearch_backend_settings, mongo_backend_settings, rq_queue_settings, celery_queue_settings, \
    empty_settings


class TestUtils(object):

    @pytest.mark.parametrize('backend_path_module, backend_class', [
        ('kaneda.backends.ElasticsearchBackend', ElasticsearchBackend),
        ('kaneda.backends.MongoBackend', MongoBackend),
        ('kaneda.backends.LoggerBackend', LoggerBackend)
    ])
    def test_import_backend_class(self, backend_path_module, backend_class):
        assert import_class(backend_path_module) is backend_class

    @pytest.mark.parametrize('backend_settings, backend_class', [
        (elasticsearch_backend_settings(), ElasticsearchBackend),
        (mongo_backend_settings(), MongoBackend),
    ])
    def test_get_backend_from_settings(self, backend_settings, backend_class):
        assert isinstance(get_object_from_settings(backend_settings.BACKEND, backend_settings), backend_class)

    @pytest.mark.parametrize('queue_path_module, queue_class', [
        ('kaneda.queues.RQQueue', RQQueue),
        ('kaneda.queues.CeleryQueue', CeleryQueue)
    ])
    def test_import_queue_class(self, queue_path_module, queue_class):
        assert import_class(queue_path_module) is queue_class

    @pytest.mark.parametrize('queue_settings, queue_class', [
        (rq_queue_settings(), RQQueue),
        (celery_queue_settings(), CeleryQueue),
    ])
    def test_get_queue_from_settings(self, queue_settings, queue_class):
        assert isinstance(get_object_from_settings(queue_settings.QUEUE, queue_settings), queue_class)

    def test_get_object_from_settings_with_error(self, unexisting_backend_settings):
        with pytest.raises(UnexistingKanedaClass):
            get_object_from_settings(unexisting_backend_settings.BACKEND, unexisting_backend_settings)

    @pytest.mark.parametrize('settings, has_backend, has_queue', [
        (elasticsearch_backend_settings(), True, False),
        (rq_queue_settings(), False, True),
    ])
    def test_get_kaneda_objects(self, mocker, settings, has_backend, has_queue):
        mock_get_settings = mocker.patch('kaneda.utils.get_settings')
        mock_get_settings.return_value = settings
        backend, queue = get_kaneda_objects()
        assert bool(backend) == has_backend
        assert bool(queue) == has_queue

    @pytest.mark.parametrize('retrieval_function', [get_backend, get_kaneda_objects])
    @pytest.mark.parametrize('settings, error_first_word', [
        (None, 'Define'),
        (empty_settings(), 'You'),
    ])
    def test_retrieval_functions_with_errors(self, mocker, retrieval_function, settings, error_first_word):
        if settings:
            mock_get_settings = mocker.patch('kaneda.utils.get_settings')
            mock_get_settings.return_value = settings
        with pytest.raises(SettingsError) as error:
            retrieval_function()
        assert str(error.value).startswith(error_first_word)
