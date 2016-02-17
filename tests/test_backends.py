from unittest.mock import patch

import pytest


class TestBackends(object):

    @pytest.fixture
    def simple_payload(self):
        return {'name': 'backend.test', 'metric':  'simple_payload', 'value': 1, 'host': 'test'}

    @pytest.fixture
    def structured_payload(self):
        return {'name': 'backend.test', 'metric':  'structured_payload', 'val0': 1, 'val2': 'str', 'val3': [1, 2],
                'host': 'test', 'tags': ['tag1', 'tags2']}

    @patch('socket.gethostname')
    def test_base_backend_simple_payload(self, mock_gethostname, dummy_backend, simple_payload):
        mock_gethostname.return_value = 'test'
        dummy_backend.report(name='backend.test', metric='simple_payload', value=1, tags=None)
        reported_data = dummy_backend.reported_data.pop()
        assert reported_data == simple_payload

    @patch('socket.gethostname')
    def test_base_backend_structured_payload(self, mock_gethostname, dummy_backend, structured_payload):
        mock_gethostname.return_value = 'test'
        dummy_backend.report(name='backend.test', metric='structured_payload',
                             value={'val0': 1, 'val2': 'str', 'val3': [1, 2]}, tags=['tag1', 'tags2'])
        reported_data = dummy_backend.reported_data.pop()
        assert reported_data == structured_payload

