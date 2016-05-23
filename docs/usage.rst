Usage
=====

You need to install `Kaneda` package::

    pip install kaneda


Backend reporting
~~~~~~~~~~~~~~~~~

You need a backend in order to keep data in a persistent storage. You can use builtin :doc:`backends`
or define your custom backend subclassing the :code:`BaseBackend` class.

The following example it shows how to send metrics with Elasticsearch as a backend::

    from kaneda.backend import ElasticsearchBackend
    from kaneda import Metrics

    backend = ElasticsearchBackend(index_name='myindex', app_name='myapp', host='localhost',
                                   port=9200, user='kaneda', password='kaneda')
    metrics = Metrics(backend=backend)
    metrics.gauge('answer_of_life', 42)

A backend class can also be instantiated passing a previously defined connection client. This is specially useful when
you want to use a tuned connection::

    client = Elasticsearch(['localhost'], port=9200, http_auth=('kaneda', 'kaneda'), timeout=0.3)
    backend = ElasticsearchBackend(index_name='myindex', app_name='myapp', client=client)

.. _async:

Asynchronous reporting
~~~~~~~~~~~~~~~~~~~~~~

Depending the selection of the backend the process of reporting metrics could be "slow" if the response time of your
application is critical (e.g: a website). Furthermore if your application doesn't need the see the reported metrics
in real time you probably have to consider to using asynchronous reporting. With this system you are allowed to send a
metric report in background without adding too much overhead.

To use this system you need to install a queue system and use one of the builtin Kaneda :ref:`queues` classes.
To setup Kaneda in async mode follow these steps.

1. Install and configure your queue system (e.g: :ref:`rq`).

.. code-block:: shell

    pip install rq

2. Setup your backend configuration in new file named :file:`kanedasettings.py`.

.. code-block:: python

    BACKEND = 'kaneda.backends.ElasticsearchBackend'
    ELASTIC_INDEX_NAME = 'myindex'
    ELASTIC_APP_NAME = 'myapp'
    ELASTIC_HOST = 'localhost'
    ELASTIC_PORT = 9200
    ELASTIC_USER = 'kaneda'
    ELASTIC_PASSWORD = 'kaneda'

3. Run the worker

.. code-block:: shell

    rqworker

Now you can use Kaneda with the same :ref:`metrics` API::

    from kaneda.queues import RQQueue
    from kaneda import Metrics

    queue = RQQueue(redis_url='redis://localhost:6379/0')
    metrics = Metrics(queue=queue)
    metrics.gauge('answer_of_life', 42)

As in the backend example it can be used passing a queue client::

    q = Queue(queue_name, connection=Redis())
    queue = RQQueue(queue=q)

Also you are able to specify a Redis connection url (or a broker url if you use :ref:`Celery`). Notice this allows you
to run the worker on a different server.