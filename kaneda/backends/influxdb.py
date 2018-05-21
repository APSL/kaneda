from __future__ import absolute_import

import logging
from datetime import datetime

try:
    from influxdb import InfluxDBClient
except ImportError:
    InfluxDBClient = None

from kaneda.exceptions import ImproperlyConfigured

from .base import BaseBackend


class InfluxBackend(BaseBackend):
    """
    InfluxDB backend.

    :param database: name of the InfluxDB database.
    :param client: client instance of InfluxDBClient class.
    :param connection_url: InfluxDB connection url (influxdb://username:password@localhost:8086/databasename).
    :param host: server host.
    :param port: server port.
    :param username: auth username.
    :param password: auth password.
    :param timeout: InfluxDB connection timeout (seconds).
    """
    settings_namespace = 'INFLUX'

    def __init__(self, database, client=None, connection_url=None, host=None, port=None, username=None, password=None,
                 timeout=0.3):
        if not InfluxDBClient:
            raise ImproperlyConfigured('You need to install the influxdb library to use the InfluxDB backend.')
        if client:
            if not isinstance(client, InfluxDBClient):
                raise ImproperlyConfigured('"client" parameter is not an instance of InfluxDBClient client.')
            self.client = client
        elif connection_url:
            self.client = InfluxDBClient.from_dsn(connection_url, timeout=timeout)
        else:
            self.client = InfluxDBClient(host=host, port=port, username=username, password=password,
                                         database=database, timeout=timeout)
        self.client.create_database(database)

    def _get_payload(self, name, value, metric, tags, id_):
        if tags:
            tags['host'] = self._get_host_name()
        else:
            tags = {'host': self._get_host_name()}
        if isinstance(value, dict):
            fields = value
            fields['name'] = name
        else:
            fields = {'name': name, 'value': value}
        return [{'measurement': metric, 'time': datetime.utcnow(), 'tags': tags, 'fields': fields}]

    def report(self, name, metric, value, tags, id_):
        try:
            payload = self._get_payload(name, value, metric, tags, id_)
            return self.client.write_points(payload)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
