Settings
========

Kaneda can be used with a settings file as the same way to use with :ref:`Django <django>`. Simply define a
:file:`kanedasettings.py` file with the backend or queue settings. Alternatively you can define the environment variable
`DEFAULT_SETTINGS_ENVAR`  pointing to the desired settings filename.

With this you will be able to use :ref:`Metrics` class without passing parameters::

    from kaneda import Metrics

    metrics = Metrics()
    metrics.gauge('answer_of_life', 42)

Backends settings
~~~~~~~~~~~~~~~~~

General
-------
BACKEND
  Class name of the backend. Available options are:

  * :code:`kaneda.backends.ElasticsearchBackend`
  * :code:`kaneda.backends.MongoBackend`
  * :code:`kaneda.backends.LoggerBackend`

Elasticsearch
-------------
ELASTIC_INDEX_NAME
  Name of the Elasticsearch index used to store metrics data. Default name format will be app_name-YYYY.MM.DD.

ELASTIC_APP_NAME
  Name of the app/project where metrics are used.

ELASTIC_CONNECTION_URL
  Elasticsearch connection url (https://user:secret@localhost:9200).

ELASTIC_HOST
  Server host.

ELASTIC_PORT
  Server port.

ELASTIC_USER
  HTTP auth username.

ELASTIC_PASSWORD
  HTTP auth password.

ELASTIC_TIMEOUT
  Elasticsearch connection timeout (seconds).

MongoDB
-------
MONGO_DB_NAME
  Name of the MongoDB database.

MONGO_COLLECTION_NAME
  Name of the MongoDB collection used to store metric data.

MONGO_CONNECTION_URL
  Mongo connection url (mongodb://localhost:27017/).

MONGO_HOST
  Server host.

MONGO_PORT
  Server port.

MONGO_TIMEOUT
  MongoDB connection timeout (milliseconds).

Logger
------
LOGGER_FILENAME
  Name of the file where logger will store the metrics.

Queues settings
~~~~~~~~~~~~~~~

General
-------
QUEUE
  Class name of the queue. Available options are:

  * :code:`kaneda.backends.CeleryQueue`
  * :code:`kaneda.backends.RQQueue`

Celery
------
CELERY_BROKER
  Broker connection url.

CELERY_QUEUE_NAME
  Name of the Celery queue.

RQ
--
RQ_REDIS_URL
  Redis connection url.

RQ_QUEUE_NAME
  Name of the RQ queue.