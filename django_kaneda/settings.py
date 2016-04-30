from django.conf import settings

BACKEND = getattr(settings, 'KANEDA_BACKEND', None)
QUEUE = getattr(settings, 'KANEDA_QUEUE', None)

# Elasticsearch backend settings
ELASTIC_INDEX_NAME = getattr(settings, 'KANEDA_ELASTIC_INDEX_NAME', 'kaneda')
ELASTIC_APP_NAME = getattr(settings, 'KANEDA_ELASTIC_APP_NAME', 'default')
ELASTIC_CONNECTION_URL = getattr(settings, 'KANEDA_ELASTIC_CONNECTION_URL', None)
ELASTIC_HOST = getattr(settings, 'KANEDA_ELASTIC_HOST', None)
ELASTIC_PORT = getattr(settings, 'KANEDA_ELASTIC_PORT', None)
ELASTIC_USER = getattr(settings, 'KANEDA_ELASTIC_USER', None)
ELASTIC_PASSWORD = getattr(settings, 'KANEDA_ELASTIC_PASSWORD', None)
ELASTIC_TIMEOUT = getattr(settings, 'KANEDA_ELASTIC_TIMEOUT', 0.3)

# MongoDB backend settings
MONGO_DB_NAME = getattr(settings, 'KANEDA_MONGO_DB_NAME', 'kaneda')
MONGO_COLLECTION_NAME = getattr(settings, 'KANEDA_MONGO_COLLECTION_NAME', 'default')
MONGO_CONNECTION_URL = getattr(settings, 'KANEDA_MONGO_CONNECTION_URL', None)
MONGO_HOST = getattr(settings, 'KANEDA_MONGO_HOST', None)
MONGO_PORT = getattr(settings, 'KANEDA_MONGO_PORT', None)
MONGO_TIMEOUT = getattr(settings, 'KANEDA_MONGO_TIMEOUT', 300)

# RethinkDB backend settings
RETHINK_DB = getattr(settings, 'KANEDA_RETHINK_DB', 'kaneda')
RETHINK_TABLE_NAME = getattr(settings, 'KANEDA_RETHINK_TABLE_NAME', None)
RETHINK_HOST = getattr(settings, 'KANEDA_RETHINK_HOST', None)
RETHINK_PORT = getattr(settings, 'KANEDA_RETHINK_PORT', None)
RETHINK_USER = getattr(settings, 'KANEDA_RETHINK_USER', None)
RETHINK_PASSWORD = getattr(settings, 'KANEDA_RETHINK_PASSWORD', None)
RETHINK_TIMEOUT = getattr(settings, 'KANEDA_RETHINK_TIMEOUT', 300)

# InfluxDB backend settings
INFLUX_DATABASE = getattr(settings, 'KANEDA_INFLUX_DATABASE', 'kaneda')
INFLUX_CONNECTION_URL = getattr(settings, 'KANEDA_INFLUX_CONNECTION_URL', None)
INFLUX_HOST = getattr(settings, 'KANEDA_INFLUX_HOST', None)
INFLUX_PORT = getattr(settings, 'KANEDA_INFLUX_PORT', None)
INFLUX_USERNAME = getattr(settings, 'KANEDA_INFLUX_USERNAME', None)
INFLUX_PASSWORD = getattr(settings, 'KANEDA_INFLUX_PASSWORD', None)
INFLUX_TIMEOUT = getattr(settings, 'KANEDA_INFLUX_TIMEOUT', 300)

# Debug backend mode settings
DEBUG = getattr(settings, 'KANEDA_DEBUG', False)
LOGGER = getattr(settings, 'KANEDA_LOGGER', None)
LOGGER_FILENAME = getattr(settings, 'KANEDA_LOGGER_FILENAME', None)

# Celery queue settings
CELERY_BROKER = getattr(settings, 'KANEDA_CELERY_BROKER', '')
CELERY_QUEUE_NAME = getattr(settings, 'KANEDA_CELERY_QUEUE_NAME', '')

# RQ queue settings
RQ_REDIS_URL = getattr(settings, 'KANEDA_RQ_REDIS_URL', 'kaneda')
RQ_QUEUE_NAME = getattr(settings, 'KANEDA_RQ_QUEUE_NAME', None)

# ZMQ queue settings
ZMQ_CONNECTION_URL = getattr(settings, 'KANEDA_ZMQ_CONNECTION_URL', '')
ZMQ_TIMEOUT = getattr(settings, 'KANEDA_ZMQ_TIMEOUT', 300)
