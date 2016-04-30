from kaneda import Metrics


class TestQueues(object):

    def test_celery(self, celery_queue):
        metrics = Metrics(queue=celery_queue)
        result = metrics.gauge('test_gauge_celery', 1)
        assert result

    def test_rq(self, rq_queue):
        metrics = Metrics(queue=rq_queue)
        result = metrics.gauge('test_gauge_rq', 1)
        assert result

    def test_zmq(self, zmq_queue):
        metrics = Metrics(queue=zmq_queue)
        metrics.gauge('test_gauge_rq', 1)
        zmq_queue.socket.close()
