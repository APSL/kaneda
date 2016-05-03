from __future__ import absolute_import

import logging

try:
    from celery import Celery
except ImportError:
    Celery = None

from kaneda.exceptions import ImproperlyConfigured

from .base import BaseQueue


class CeleryQueue(BaseQueue):
    """
    Celery queue.

    :param app: app instance of Celery class.
    :param broker: broker connection url where Celery will attend the async reporting requests.
    :param queue_name: name of the queue being used by the Celery worker process.
    """
    settings_namespace = 'CELERY'

    def __init__(self, app=None, broker=None, queue_name=''):
        if not Celery:
            raise ImproperlyConfigured('You need to install the celery library to use Celery queue.')
        if app:
            if not isinstance(app, Celery):
                raise ImproperlyConfigured('"queue" parameter is not an instance of Celery queue.')
            self.app = app
        else:
            self.app = Celery(broker=broker)
        self.queue_name = queue_name

    def report(self, name, metric, value, tags, id_):
        try:
            return self.app.send_task('kaneda.tasks.celery.report', args=(name, metric, value, tags, id_),
                                      queue=self.queue_name)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
