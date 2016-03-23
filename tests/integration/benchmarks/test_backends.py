from kaneda import Metrics


class TestBenchmarksBackends(object):

    def test_benchmark_elasticsearch(self, elasticsearch_backend, benchmark):
        metrics = Metrics(backend=elasticsearch_backend)
        benchmark(metrics.gauge, 'benchmark_elasticsearch', 1)

    def test_benchmark_mongo(self, mongo_backend, benchmark):
        metrics = Metrics(backend=mongo_backend)
        benchmark(metrics.gauge, 'benchmark_mongo', 1)
