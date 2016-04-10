Usage
=====

You need to install `Kaneda` package::

    pip install git+https://gitlab.apsl.net/apsl/kaneda.git


Then you need a backend in order to keep data in a persistent storage. You can use builtin :doc:`backends`
or define your custom backend subclassing the :code:`BaseBackend` class.

The following example it shows how to send metrics with Elasticsearch as a backend::

    from kaneda.backend import ElasticsearchBackend
    from kaneda import Metrics

    backend = ElasticsearchBackend(index_name='myindex', app_name='myapp', host='localhost',
                                   port=9200, user='kaneda', password='kaneda')
    metrics = Metrics(backend)
    metrics.gauge('answer_of_life', 42)
