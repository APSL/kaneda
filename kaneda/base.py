from time import time
from functools import wraps


class Metrics(object):

    def __init__(self, backend):
        self.backend = backend

    def gauge(self, name, value, tags=None):
        """
        Record the value of a gauge.

        >>> metrics.gauge('users.notifications', 13, tags=['', ''])
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

        >>> metrics.custom('hotel.availability.response_data', metric='xml', value={'status': 'ok', 'xml': ...}, id_='2B75D750')
        """
        self._report(name, metric, value, tags, id_)

    class _TimedContextManagerDecorator(object):
        """
        A context manager and a decorator which will report the elapsed time in
        the context OR in a function call.
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
                self.name = '%s.%s' % (func.__module__, func.__name__)

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
        A decorator or context manager that will measure the distribution of a
        function's/context's run time. If the metric is not defined as a decorator, the module
        name and function name will be used.
        ::

            @metrics.timed('user.query.time')
            def get_user(user_id):
                # Do what you need to ...
                pass

            # Is equivalent to ...
            with metrics.timed('user.query.time'):
                # Do what you need to ...
                pass

            # Is equivalent to ...
            start = time.time()
            try:
                get_user(user_id)
            finally:
                metrics.timing('user.query.time', time.time() - start)
        """
        return self._TimedContextManagerDecorator(self, name, tags, use_ms)

    def _report(self, name, metric, value, tags, id_=None):
        self.backend.report(name, metric, value, tags, id_)
