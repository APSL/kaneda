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
