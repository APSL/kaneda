Django Setup
============

Kaneda can be use with Django as a mechanism to reporting metrics and events.

1. Install `kaneda` and `django-kaneda` packages::

    pip install git+https://gitlab.apsl.net/apsl/kaneda.git
    pip install git+https://gitlab.apsl.net/apsl/django-kaneda.git

2. Add :code:`django_kaneda` to :code:`INSTALLED_APPS` in :file:`settings.py`.

3. Set :code:`KANEDA_BACKEND` and the properly configuration of your selected backend in :file:`settings.py`. If we want
to use Elasticsearch our configuration will be something like this::

    KANEDA_BACKEND = 'kaneda.backends.ElasticsearchBackend'
    KANEDA_ELASTIC_INDEX_NAME = 'kaneda'
    KANEDA_ELASTIC_APP_NAME = 'YouProject'
    KANEDA_ELASTIC_HOST = 'localhost'
    KANEDA_ELASTIC_PORT = 9200
    KANEDA_ELASTIC_USER = 'user'
    KANEDA_ELASTIC_PASSWORD = 'pass'

With this, you can use Kaneda in everyplace of your Django project::

    from django_kaneda import metrics


    class UserProfileView(TemplateView):
        template_name = 'user/profile.html'

        @metrics.timed('user_profile.time')
        def get(self, request, *args, **kwargs):
            metrics.increment('user_profile.views')
            return super(UserProfileView, self).get(request, *args, **kwargs)


Available settings
~~~~~~~~~~~~~~~~~~
Elasticsearch
-------------
ELASTIC_INDEX_NAME (='kaneda')
  name of the Elasticsearch index used to store metrics data. Default name format will be app_name-YYYY.MM.DD.

ELASTIC_APP_NAME (='default')
  name of the app/project where metrics are used.

ELASTIC_HOST (='localhost')
  server host.

ELASTIC_PORT (=9200)
  server port.

ELASTIC_USER (=None)
  http auth username.

ELASTIC_PASSWORD (=None)
  http auth password.

MongoDB
-------
MONGO_DB_NAME (='kaneda')
  name of the MongoDB database.

MONGO_COLLECTION_NAME (='default')
  name of the MongoDB collection used to store metric data.

MONGO_HOST (='localhost')
  server host.

MONGO_PORT (=27017)
  server port.

MONGO_USER (=None)
  auth username.

MONGO_PASSWORD (=None)
  auth password.
