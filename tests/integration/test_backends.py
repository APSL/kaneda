import pytest

from .conftest import elasticsearch_clients, mongo_clients, rethink_clients, influx_clients


class TestBackends(object):

    @pytest.mark.parametrize('client', elasticsearch_clients())
    def test_elasticsearch_connection(self, client):
        assert client.ping()

    @pytest.mark.parametrize('client', mongo_clients())
    def test_mongo_connection(self, client):
        assert client.server_info()

    @pytest.mark.parametrize('connection', rethink_clients())
    def test_rethink_connection(self, connection):
        assert connection.is_open()

    @pytest.mark.parametrize('client', influx_clients())
    def test_influx_connection(self, client):
        try:
            assert client.get_list_database()
        except ConnectionError:
            assert False
