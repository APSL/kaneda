import pytest

from kaneda import Metrics


class TestMetricReporter(object):

    @pytest.fixture
    def metrics(self, dummy_backend):
        return Metrics(backend=dummy_backend)

    def test_gauge(self, metrics):
        metrics.gauge('users.online', 123)

    def test_increment(self, metrics):
        metrics.increment('page.views')

    def test_decrement(self, metrics):
        metrics.decrement('page.views')

    def test_timing(self, metrics):
        metrics.timing('query.response.time', 1234)

    def test_event(self, metrics):
        metrics.event('Man down!', 'This server needs assistance.')

    def test_custom(self, metrics):
        metrics.custom(name='availability.request', metric='xml_response', id_='2B75D750',
                       value={'status': 'ok', 'xml': '<xml><test attr="test"></test></xml>'}, tags=['test'])

    def test_timed_context_manager(self, metrics):
        with metrics.timed('user.query.time', use_ms=True):
            pass

    def test_timed_decorator(self, metrics):
        @metrics.timed('user.query.time', use_ms=False)
        def get_user():
            pass
        get_user()
