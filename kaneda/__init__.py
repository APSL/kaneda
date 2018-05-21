# -*- coding: utf-8 -*-
__author__ = 'Marc Tudurí'
__email__ = 'mtuduri@apsl.net'
__version__ = '1.0'

import logging  # NOQA

from .base import Metrics  # NOQA

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
logging.getLogger(__name__).addHandler(NullHandler())
