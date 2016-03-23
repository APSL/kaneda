from __future__ import absolute_import

import logging
from datetime import datetime

try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None

from kaneda.exceptions import ImproperlyConfigured

from .base import BaseBackend


class MongoBackend(BaseBackend):
    """
    MongoDB backend.

    :param db_name: name of the MongoDB database.
    :param collection_name: name of the MongoDB collection used to store metric data.
    :param client: client instance of MongoClient class.
    :param connection_url: Mongo connection url (mongodb://localhost:27017/).
    :param host: server host.
    :param port: server port.
    :param timeout: MongoDB connection timeout (milliseconds).
    """
    settings_namespace = 'MONGO'

    def __init__(self, db_name, collection_name, client=None, connection_url=None, host=None, port=None, timeout=300):
        if not MongoClient:
            raise ImproperlyConfigured('You need to install the pymongo library to use the MongoDB backend.')
        if client:
            if not isinstance(client, MongoClient):
                raise ImproperlyConfigured('"client" parameter is not an instance of MongoClient client.')
            self.client = client
        elif connection_url:
            self.client = MongoClient(connection_url, serverSelectionTimeoutMS=timeout)
        else:
            self.client = MongoClient(host=host, port=port, serverSelectionTimeoutMS=timeout)
        db = self.client[db_name]
        self.collection = db[collection_name]

    def _get_payload(self, name, value, metric, tags, id_):
        payload = super(MongoBackend, self)._get_payload(name, value, tags)
        payload['timestamp'] = datetime.utcnow()
        payload['metric'] = metric
        if id_:
            payload['_id'] = id_
        return payload

    def report(self, name, metric, value, tags, id_):
        payload = self._get_payload(name, value, metric, tags, id_)
        try:
            return self.collection.insert_one(payload)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
