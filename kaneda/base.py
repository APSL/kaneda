from __future__ import absolute_import

from time import time
from functools import wraps

from kaneda.utils import get_kaneda_objects


class Metrics(object):
    """
    Metrics reporting class

    :param backend: instance of kaneda.backends. It is the responsible to store the reported data.
    :param queue: instance of kaneda.queues. It is the responsible to store the reported data asynchronously.

    If none of the parameters are passed it tries get the backend from kaneda settings file.
    """
    def __init__(self, backend=None, queue=None):
        self.backend = backend
        self.queue = queue
        if not self.backend and not self.queue:
            self.backend, self.queue = get_kaneda_objects()

    def gauge(self, name, value, tags=None):
        """
        Record the value of a gauge.

        >>> metrics.gauge('users.notifications', 13, tags=['new_message', 'follow_request'])
        """
        return self._report(name, 'gauge', value, tags)

    def increment(self, name, tags=None):
        """
        Increment a counter.

        >>> metrics.increment('user.profile.views')
        """
        self._report(name, 'counter', 1, tags)

    def decrement(self, name, tags=None):
        """
        Decrement a counter.

        >>> metrics.decrement('hotel.occupation')
        """
        self._report(name, 'counter', -1, tags)

    def timing(self, name, value, tags=None):
        """
        Record a timing.

        >>> metrics.timing('hotel.availability.request_time', 4)
        """
        self._report(name, 'timing', value, tags)

    def event(self, name, text, tags=None):
        """
        Record an event.

        >>> metrics.event('user.signup', 'New user registered')
        """
        self._report(name, 'event', text, tags)

    def custom(self, name, metric, value, tags=None, id_=None):
        """
        Send a custom metric report.

        >>> metrics.custom('hotel.response_data', metric='xml', value={'status': 'ok', 'xml': ...}, id_='2B75D750')
        """
        self._report(name, metric, value, tags, id_)

    class _TimedContextManagerDecorator(object):
        """
        Class that implements the context manager and the decorator for "timed" method.
        """

        def __init__(self, metrics, name=None, tags=None, use_ms=None):
            self.metrics = metrics
            self.name = name
            self.tags = tags
            self.use_ms = use_ms

        def __call__(self, func):
            """
            Decorator which returns the elapsed time of the function call.
            """
            if not self.name:
                self.name = u'{0:s}.{1:s}'.format(func.__module__, func.__name__)

            @wraps(func)
            def wrapped(*args, **kwargs):
                with self:
                    return func(*args, **kwargs)
            return wrapped

        def __enter__(self):
            self.start = time()

        def __exit__(self, type, value, traceback):
            elapsed = time() - self.start
            elapsed = int(round(1000 * elapsed)) if self.use_ms else elapsed
            self.metrics.timing(self.name, elapsed, self.tags)

    def timed(self, name=None, tags=None, use_ms=None):
        """
        Measure the amount of time of a function (using a decorator) or a piece of
        code (using a context manager). If name is not provided while using the decorator it
        will be used the name of the module and the function.
        ::

            # With decorator
            @metrics.timed('request.response_time')
            def perform_request(params):
                pass

            # With context manager
            with metrics.timed('request.response_time'):
                pass
        """
        return self._TimedContextManagerDecorator(self, name, tags, use_ms)

    def _report(self, name, metric, value, tags, id_=None):
        if self.backend:
            return self.backend.report(name, metric, value, tags, id_)
        elif self.queue:
            return self.queue.report(name, metric, value, tags, id_)
