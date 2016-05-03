from kaneda import Metrics


class TestMetrics(object):

    def test_elasticsearch_metric(self, elasticsearch_backend):
        metrics = Metrics(backend=elasticsearch_backend)
        result = metrics.gauge('test_gauge', 42)
        assert result
        assert result['_id']

    def test_mongo_metric(self, mongo_backend):
        metrics = Metrics(backend=mongo_backend)
        result = metrics.gauge('test_gauge', 42)
        assert result
        assert result.inserted_id

    def test_logger_metric(self, logger_backend, logger_filename):
        metrics = Metrics(backend=logger_backend)
        metrics.gauge('test_gauge', 42)
        with open(logger_filename) as f:
            lines = f.readlines()
            assert lines
            result = lines[-1].split(' - ')[2]
            assert result
            assert 'test_gauge' in result
