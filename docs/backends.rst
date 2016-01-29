Backends
========

Kaneda provides bultin backends to store metrics and events in a persistent storage. If you want to use your
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
