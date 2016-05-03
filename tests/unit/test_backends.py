import pytest


class TestBackends(object):

    @pytest.fixture
    def simple_payload(self):
        return {'name': 'test.simple', 'metric':  'simple_payload', 'value': 1, 'host': 'test'}

    @pytest.fixture
    def structured_payload(self):
        return {'name': 'test.structured', 'metric':  'structured_payload', 'val0': 1, 'val2': 'str', 'val3': [1, 2],
                'host': 'test', 'tags': ['tag1', 'tags2']}

    def test_base_backend_simple_payload(self, mocker, dummy_backend, simple_payload):
        mock_gethostname = mocker.patch('socket.gethostname')
        mock_gethostname.return_value = 'test'
        dummy_backend.report(name='test.simple', metric='simple_payload', value=1, tags=None)
        reported_data = dummy_backend.reported_data['test.simple']
        assert reported_data == simple_payload

    def test_base_backend_structured_payload(self, mocker, dummy_backend, structured_payload):
        mock_gethostname = mocker.patch('socket.gethostname')
        mock_gethostname.return_value = 'test'
        dummy_backend.report(name='test.structured', metric='structured_payload',
                             value={'val0': 1, 'val2': 'str', 'val3': [1, 2]}, tags=['tag1', 'tags2'])
        reported_data = dummy_backend.reported_data['test.structured']
        assert reported_data == structured_payload
