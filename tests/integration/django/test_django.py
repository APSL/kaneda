from kaneda.backends import LoggerBackend, ElasticsearchBackend
from kaneda.queues import CeleryQueue
from django_kaneda import settings  # NOQA


class TestDjango(object):

    def test_django_kaneda_with_backend(self, mocker, django_settings_backend):
        mocker.patch('django_kaneda.settings', django_settings_backend)
        from django_kaneda import LazyMetrics
        metrics = LazyMetrics()
        assert isinstance(metrics.backend, ElasticsearchBackend)
        result = metrics.gauge('test_gauge', 42)
        assert result

    def test_django_kaneda_with_debug(self, mocker, django_settings_debug):
        mocker.patch('django_kaneda.settings', django_settings_debug)
        from django_kaneda import LazyMetrics
        metrics = LazyMetrics()
        metrics.gauge('test_gauge', 42)
        assert isinstance(metrics.backend, LoggerBackend)

    def test_django_kaneda_with_queue(self, mocker, django_settings_queue):
        mocker.patch('django_kaneda.settings', django_settings_queue)
        from django_kaneda import LazyMetrics
        metrics = LazyMetrics()
        assert isinstance(metrics.queue, CeleryQueue)
        result = metrics.gauge('test_gauge', 42)
        assert result
