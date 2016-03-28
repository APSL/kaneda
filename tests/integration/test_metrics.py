from kaneda import Metrics


class TestMetrics(object):

    def test_elasticsearch_gauge(self, elasticsearch_backend):
        value = 42
        metrics = Metrics(backend=elasticsearch_backend)
        metrics.gauge('test_gauge', value)
        result = elasticsearch_backend.client.search(index=elasticsearch_backend._get_index_name(), doc_type='gauge')
        assert result
        assert result['hits']['hits'][0]['_source']['value'] == value
        assert result['hits']['hits'][0]['_source']['name'] == 'test_gauge'

    def test_mongo_gauge(self, mongo_backend):
        value = 42
        metrics = Metrics(backend=mongo_backend)
        metrics.gauge('test_gauge', value)
        result = mongo_backend.collection.find_one({"metric": 'gauge'})
        assert result
        assert result['value'] == value
        assert result['name'] == 'test_gauge'

    def test_logger_gauge(self, logger_backend, logger_filename):
        value = 42
        metrics = Metrics(backend=logger_backend)
        metrics.gauge('test_gauge', value)
        with open(logger_filename) as f:
            lines = f.readlines()
            assert lines
            result = lines[-1].split(' - ')[2]
            assert result
            assert str(value) in result
            assert 'test_gauge' in result




