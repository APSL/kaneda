.. _django:

Django Setup
============

Kaneda can be use with Django as a mechanism to reporting metrics and events.

1. Add :code:`django_kaneda` to :code:`INSTALLED_APPS` in :file:`settings.py`.

2. Set :code:`KANEDA_BACKEND` and the properly configuration of your selected backend in :file:`settings.py`. If you want to use Elasticsearch our configuration will be something like this::

    KANEDA_BACKEND = 'kaneda.backends.ElasticsearchBackend'
    KANEDA_ELASTIC_INDEX_NAME = 'kaneda'
    KANEDA_ELASTIC_APP_NAME = 'YouProject'
    KANEDA_ELASTIC_HOST = 'localhost'
    KANEDA_ELASTIC_PORT = 9200
    KANEDA_ELASTIC_USER = 'user'
    KANEDA_ELASTIC_PASSWORD = 'pass'

Alternatively you can set :code:`KANEDA_QUEUE` to specify a :ref:`queue <queues>` configuration to use Kaneda in :ref:`async mode <async>`::

    KANEDA_QUEUE = 'kaneda.queues.CeleryQueue'
    KANEDA_CELERY_BROKER = 'redis://localhost:6379/0'

With this, you can use Kaneda in everyplace of your Django project::

    from django_kaneda import metrics


    class UserProfileView(TemplateView):
        template_name = 'user/profile.html'

        @metrics.timed('user_profile.time')
        def get(self, request, *args, **kwargs):
            metrics.increment('user_profile.views')
            return super(UserProfileView, self).get(request, *args, **kwargs)

Debug mode
~~~~~~~~~~
You can use Kaneda in debug mode with a logger as backend. Simply set :code:`KANEDA_DEBUG` to `True` to report everything
to a logger instead a persistent backend. Furthermore, you can set a previously defined logger on :file:`settings.py` and use as
your debug logger::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'with_timestamp': {
                'format': '%(asctime)s - %(name)s - %(message)s'
            }
        },
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': '/tmp/kaneda-demo.log',
                'formatter': 'with_timestamp'
            },
        },
        'loggers': {
            'kaneda.demo': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }

    KANEDA_DEBUG = True
    KANEDA_LOGGER = 'kaneda.demo'

Alternatively you can set :code:`KANEDA_LOGGER_FILENAME` instead of :code:`KANEDA_LOGGER` to store the reporting results
in a specific filename.

Available settings
~~~~~~~~~~~~~~~~~~
Elasticsearch
-------------
KANEDA_ELASTIC_INDEX_NAME (='kaneda')
  Name of the Elasticsearch index used to store metrics data. Default name format will be app_name-YYYY.MM.DD.

KANEDA_ELASTIC_APP_NAME (='default')
  Name of the app/project where metrics are used.

KANEDA_ELASTIC_CONNECTION_URL (=None)
  Elasticsearch connection url (https://user:secret@localhost:9200).

KANEDA_ELASTIC_HOST (=None)
  Server host.

KANEDA_ELASTIC_PORT (=None)
  Server port.

KANEDA_ELASTIC_USER (=None)
  HTTP auth username.

KANEDA_ELASTIC_PASSWORD (=None)
  HTTP auth password.

KANEDA_ELASTIC_TIMEOUT (=0.3)
  Elasticsearch connection timeout (seconds).

MongoDB
-------
KANEDA_MONGO_DB_NAME (='kaneda')
  Name of the MongoDB database.

KANEDA_MONGO_COLLECTION_NAME (='default')
  Name of the MongoDB collection used to store metric data.

KANEDA_MONGO_CONNECTION_URL (=None)
  Mongo connection url (mongodb://localhost:27017/).

KANEDA_MONGO_HOST (=None)
  Server host.

KANEDA_MONGO_PORT (=None)
  Server port.

KANEDA_MONGO_TIMEOUT (=300)
  MongoDB connection timeout (milliseconds).

RethinkDB
---------
KANEDA_RETHINK_DB (='kaneda')
  Name of the RethinkDB database

KANEDA_RETHINK_TABLE_NAME (=None)
  Name of the RethinkDB table. If this is not provided, it will be used the name of the metric.

KANEDA_RETHINK_HOST (=None)
  Server host.

KANEDA_RETHINK_PORT (=None)
  Server port.

KANEDA_RETHINK_USER (=None)
  Auth username.

KANEDA_RETHINK_PASSWORD (=None)
  Auth password.

KANEDA_RETHINK_TIMEOUT (=0.3)
  RethinkDB connection timeout (seconds).

InfluxDB
--------
KANEDA_INFLUX_DATABASE (='kaneda')
  Name of the InfluxDB database.

KANEDA_INFLUX_CONNECTION_URL (=None)
  InfluxDB connection url (influxdb://username:password@localhost:8086/databasename).

KANEDA_INFLUX_HOST (=None)
  Server host.

KANEDA_INFLUX_PORT (=None)
  Server port.

KANEDA_INFLUX_USERNAME (=None)
  Auth username.

KANEDA_INFLUX_PASSWORD (=None)
  Auth password.

KANEDA_INFLUX_TIMEOUT (=0.3)
  InfluxDB connection timeout (seconds).

Celery
------
KANEDA_CELERY_BROKER (='')
  Broker connection url.

KANEDA_CELERY_QUEUE_NAME (='')
  Name of the Celery queue.

RQ
--
KANEDA_RQ_REDIS_URL (='')
  Redis connection url.

KANEDA_RQ_QUEUE_NAME (='kaneda')
  Name of the RQ queue.

ZMQ
---
KANEDA_ZMQ_CONNECTION_URL (='')
  ZMQ connection url.

KANEDA_ZMQ_TIMEOUT (=300)
  ZMQ socket timeout (milliseconds).

Debug
-----
KANEDA_DEBUG (=True)
  Use Kaneda in debug mode.

KANEDA_LOGGER (=None)
  Name of a previously defined logger, to use in debug mode.

KANEDA_LOGGER_FILENAME (=None)
  Name of the file where logger will store the metrics, to use in debug mode.
