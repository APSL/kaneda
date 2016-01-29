Kaneda
======

Kaneda is a Python library that allows to get, report and store events and metrics of your applications.
It provides a several builtin :doc:`metrics` methods in order to store any amount of data that you want to then
analyze it or for performance studies

Example::

   from kaneda import Metrics
   metrics = Metrics(...)
   metrics.event('welcome', 'Kaneda is cool')
   metrics.gauge('answer_of_life', 42)

.. toctree::
   :hidden:

   usage
   django
   metrics
   backends
   changelog

