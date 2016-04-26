Backends
========

Kaneda provides builtin backends to store metrics and events in a persistent storage. If you want to use your
custom backend you need to subclass :code:`BaseBackend` and implement your custom :code:`report` method which
is the responsible to store the metrics data.

Elasticsearch
~~~~~~~~~~~~~

Elasticsearch is a search based NoSQL database that works very well with metrics data. It provides powerful tools to analyze data and build
real-time dashboards easily with `Kibana <https://www.elastic.co/products/kibana>`_.

.. note::

    Before using Elasticesearch as backend you need to install Elasticsearch Python client::

        pip install elasticsearch


.. autoclass:: kaneda.backends.ElasticsearchBackend
    :members:

MongoDB
~~~~~~~

MongoDB is a document oriented NoSQL database. Is a great tool to store metrics as it provides a powerful aggregation framework
to perform data analysis.

.. note::

    Before using MongoDB as backend you need to install MongoDB Python client::

        pip install pymongo


.. autoclass:: kaneda.backends.MongoBackend
    :members:

RethinkDB
~~~~~~~~~

RethinkDB is an open source scalable, distributed NoSQL database built for realtime applications.

.. note::

    Before using RethinkDB as backend you need to install RethinkDB Python client::

        pip install rethinkdb


.. autoclass:: kaneda.backends.RethinkBackend
    :members:


InfluxDB
~~~~~~~~

InfluxDB is an open source time series database with no external dependencies. It's useful for recording metrics,
events, and performing analytics.

.. note::

    Before using InfluxDB as backend you need to install InfluxDB Python client::

        pip install influxdb

.. warning::

    InfluxDB can store other type of data besides time series. However it has some restrictions:

    * Metrics *tags* field can't be a :code:`list` only a :code:`dict`::

         # bad
         metrics.timing('user.profile_load_time', 230, tags=['login', 'edit_profile'])

         # good
         metrics.timing('user.profile_load_time', 230, tags={'from': 'login', 'to': 'edit_profile'})

    * :any:`Custom <kaneda.base.Metrics.custom>` metric *value* field can’t be a :code:`list` nor a nested :code:`dict`::

         # bad
         metrics.custom('zone.search', metric='query_time', value={'times': [120, 230]})
         metrics.custom('zone.search', metric='query_time', value={'times': {'start': 120}, {'end': 230}})

         # good
         metrics.custom('zone.search', metric='query_time', value={'start_time': 120, 'end_time': 230})

.. autoclass:: kaneda.backends.InfluxBackend
    :members:

Logger
~~~~~~

You can use a logger instance of the logging library from the Python standard lib. Useful for debugging.

.. autoclass:: kaneda.backends.LoggerBackend
    :members: