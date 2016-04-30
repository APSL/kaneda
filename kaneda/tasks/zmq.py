from __future__ import absolute_import

from datetime import datetime

import click
import zmq

from kaneda.exceptions import SettingsError
from kaneda.utils import get_backend, get_settings


@click.command()
@click.option('--connection_url', '-u', help='ZMQ connection url, e.g: tcp://127.0.0.1:5555')
def zmq_task(connection_url):
    """
    ZMQ job to report metrics to the configured backend in kanedasettings.py

    To run the worker execute this command:
        zmqworker --connection_url=<zmq_connection_url>
    """
    if not connection_url:
        try:
            settings = get_settings()
            connection_url = settings.ZMQ_CONNECTION_URL
        except ImportError:
            raise SettingsError("Pass --connection_url option or define ZMQ_CONNECTION_URL on Kaneda settings file "
                                "before use ZMQ task processor.")
    backend = get_backend()
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect(connection_url)
    poller = zmq.Poller()
    poller.register(socket)
    click.secho('Running ZMQ worker - listening at {}.'.format(connection_url), fg='blue')
    click.secho('Using {}.'.format(backend.__class__.__name__), fg='blue')
    click.echo('\n')
    while True:
        events = dict(poller.poll(0))
        if socket in events:
            payload = socket.recv_json()
            click.secho('[{}: Received data] {}'.format(datetime.utcnow(), payload), fg='green')
            backend.report(**payload)
