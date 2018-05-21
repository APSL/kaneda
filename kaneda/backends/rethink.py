from __future__ import absolute_import

import logging

try:
    import rethinkdb as r
except ImportError:
    r = None

from kaneda.exceptions import ImproperlyConfigured

from .base import BaseBackend


class RethinkBackend(BaseBackend):
    """
    RethinkDB backend.

    :param db: name of the RethinkDB database.
    :param table_name: name of the RethinkDB table. If this is not provided, it will be used the name of the metric.
    :param host: server host.
    :param port: server port.
    :param user: auth username.
    :param password: auth password.
    :param timeout: RethinkDB connection timeout (seconds).
    """
    settings_namespace = 'RETHINK'

    def __init__(self, db, table_name=None, connection=None, host=None, port=None, user=None, password=None,
                 timeout=0.3):
        if not r:
            raise ImproperlyConfigured('You need to install the rethinkdb library to use the RethinkDB backend.')
        if connection:
            self.connection = connection
        elif host and port:
            if user and password:
                self.connection = r.connect(host=host, port=port, db=db, user=user, password=password, timeout=timeout)
            else:
                self.connection = r.connect(host=host, port=port, db=db, timeout=timeout)
        self.db = db
        self.table_name = table_name
        if self.connection is None:
            self.connection = r.connect(db=db, timeout=timeout)
        self._create_database()

    def _get_payload(self, name, value, tags, id_):
        payload = super(RethinkBackend, self)._get_payload(name, value, tags)
        payload['timestamp'] = r.now()
        if id_:
            payload['id'] = id_
        return payload

    def _create_database(self):
        if self.db not in r.db_list().run(self.connection):
            r.db_create(self.db).run(self.connection)

    def _create_table(self, metric):
        table_name = self._get_table_name(metric)
        if table_name not in r.db(self.db).table_list().run(self.connection):
            r.db(self.db).table_create(table_name).run(self.connection)

    def _get_table_name(self, metric):
        return self.table_name or metric

    def report(self, name, metric, value, tags, id_):
        try:
            table_name = self._get_table_name(metric)
            self._create_table(metric)
            payload = self._get_payload(name, value, tags, id_)
            return r.table(table_name).insert(payload).run(self.connection)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
