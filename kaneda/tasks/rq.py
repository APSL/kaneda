from __future__ import absolute_import

from redis import Redis
from rq.decorators import job

from kaneda.utils import get_backend

backend = get_backend()


@job(queue='kaneda', connection=Redis())
def report(name, metric, value, tags, id_):
    """
    RQ job to report metrics to the configured backend in kanedasettings.py

    To run the worker execute this command:
        rqworker [queue]
    """
    return backend.report(name, metric, value, tags, id_)
