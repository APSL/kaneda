from kaneda import Metrics

from . import mark_benchmark


@mark_benchmark
class TestQueues(object):

    def test_benchmark_celery(self, celery_queue, benchmark):
        metrics = Metrics(queue=celery_queue)
        benchmark(metrics.gauge, 'benchmark_celery', 1)

    def test_benchmark_rq(self, rq_queue, benchmark):
        metrics = Metrics(queue=rq_queue)
        benchmark(metrics.gauge, 'benchmark_rq', 1)

    def test_benchmark_zmq(self, zmq_queue, benchmark):
        metrics = Metrics(queue=zmq_queue)
        benchmark(metrics.gauge, 'benchmark_zmq', 1)
