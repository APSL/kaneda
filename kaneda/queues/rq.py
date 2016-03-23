from __future__ import absolute_import

import logging

try:
    from redis import Redis
    from rq import Queue
except ImportError:
    Redis = None
    Queue = None

from kaneda.exceptions import ImproperlyConfigured

from .base import BaseQueue


class RQQueue(BaseQueue):
    """
    RQ queue

    :param queue: queue instance of RQ class.
    :param redis_url: Redis connection url where RQ will attend the async reporting requests.
    :param queue_name: name of the queue being used by the RQ worker process.
    """
    settings_namespace = 'RQ'

    def __init__(self, queue=None, redis_url=None, queue_name='kaneda'):
        if not Redis:
            raise ImproperlyConfigured('You need to install redis to use the RQ queue.')
        if not Queue:
            raise ImproperlyConfigured('You need to install rq library to use the RQ queue.')
        if queue:
            if not isinstance(queue, Queue):
                raise ImproperlyConfigured('"queue" parameter is not an instance of RQ queue.')
            self.queue = queue
        elif redis_url:
            self.queue = Queue(queue_name, connection=Redis.from_url(redis_url))
        else:
            self.queue = Queue(queue_name, connection=Redis())

    def report(self, name, metric, value, tags, id_):
        try:
            return self.queue.enqueue('kaneda.tasks.rq.report', name, metric, value, tags, id_)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
