Kaneda
======

.. image:: https://travis-ci.org/APSL/kaneda.svg?branch=master
    :target: https://travis-ci.org/APSL/kaneda

.. image:: https://readthedocs.org/projects/kaneda/badge/?version=latest
    :target: https://readthedocs.org/projects/kaneda/?badge=latest    

Kaneda is a Python library that allows to report events and metrics of your applications.
It provides a several builtin `metrics <http://kaneda.readthedocs.io/en/latest/metrics.html>`_ methods in order to store any amount of data that you want to then
analyze it or for performance studies.

Usage
~~~~~~~~~~~

First of all, you need to install `Kaneda` package::

    pip install kaneda

Then you need a backend in order to keep data in a persistent storage.
The following example it shows how to send metrics with Elasticsearch as a backend:

.. code-block:: python

    from kaneda.backend import ElasticsearchBackend
    from kaneda import Metrics

    backend = ElasticsearchBackend(index_name='myindex', app_name='myapp', host='localhost',
                                   port=9200, user='kaneda', password='kaneda')
    metrics = Metrics(backend=backend)
    metrics.gauge('answer_of_life', 42)

Features
~~~~~~~~
* Builtin `metrics <http://kaneda.readthedocs.io/en/latest/metrics.html>`_ functions and custom metric reports.
* Configurable reporting `backends <http://kaneda.readthedocs.io/en/latest/backends.html>`_ classes and `asynchronous <http://kaneda.readthedocs.io/en/latest/queues.html>`_ queue classes.
* Builtin Elasticsearch, MongoDB, InfluxDB and RethinkDB backends.
* Builtin Celery, RQ and ZMQ asynchronous queue classes.
* Django support.

Documentation
~~~~~~~~~~~~~
Visit the `documentation <http://kaneda.readthedocs.org>`_ for an in-depth look at Kaneda.
