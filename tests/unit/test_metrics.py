from time import sleep

import pytest

from kaneda import Metrics


class TestMetrics(object):

    @pytest.fixture
    def metrics(self, dummy_backend):
        return Metrics(backend=dummy_backend)

    def assert_reported_data(self, dummy_backend, metric, name, value):
        assert dummy_backend.reported_data[name]['name'] == name
        assert dummy_backend.reported_data[name]['metric'] == metric
        if 'value' in dummy_backend.reported_data[name]:
            if isinstance(dummy_backend.reported_data[name]['value'], float):
                assert round(dummy_backend.reported_data[name]['value'], 2) == value
            else:
                assert dummy_backend.reported_data[name]['value'] == value

    def test_gauge(self, metrics, dummy_backend):
        value = 123
        metrics.gauge('users.online', value)
        self.assert_reported_data(dummy_backend, 'gauge', 'users.online', value)

    def test_increment(self, metrics, dummy_backend):
        metrics.increment('page.views')
        self.assert_reported_data(dummy_backend, 'counter', 'page.views', 1)

    def test_decrement(self, metrics, dummy_backend):
        metrics.decrement('credit.usage')
        self.assert_reported_data(dummy_backend, 'counter', 'credit.usage', -1)

    def test_timing(self, metrics, dummy_backend):
        value = 260
        metrics.timing('query.response.time', value)
        self.assert_reported_data(dummy_backend, 'timing', 'query.response.time', value)

    def test_event(self, metrics, dummy_backend):
        value = 'Too much requests'
        metrics.event('server.status', value)
        self.assert_reported_data(dummy_backend, 'event', 'server.status', value)

    def test_custom(self, metrics, dummy_backend):
        value = {'status': 'ok', 'xml': '<xml><test attr="test"></test></xml>'}
        metrics.custom(name='availability.request', metric='xml_response', id_='2B75D750', value=value, tags=['test'])
        self.assert_reported_data(dummy_backend, 'xml_response', 'availability.request', value)

    def test_timed_context_manager(self, metrics, dummy_backend):
        value = 100
        with metrics.timed('user.query.time', use_ms=True):
            sleep(value / 1000.0)  # in ms
        self.assert_reported_data(dummy_backend, 'timing', 'user.query.time', value)

    def test_timed_decorator(self, metrics, dummy_backend):
        value = 0.1

        @metrics.timed(use_ms=False)
        def get_user():
            sleep(value)
        get_user()
        self.assert_reported_data(dummy_backend, 'timing', 'tests.unit.test_metrics.get_user', value)
