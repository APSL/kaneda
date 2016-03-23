from __future__ import absolute_import

from celery import Celery

from kaneda.utils import get_backend

backend = get_backend()

app = Celery()
app.config_from_object('celeryconfig')


@app.task()
def report(name, metric, value, tags, id_):
    """
    Celery task to report metrics to the configured backend in kanedasettings.py

    To run the worker execute this command:
        celery -A kaneda.tasks.celery worker
    """
    return backend.report(name, metric, value, tags, id_)
