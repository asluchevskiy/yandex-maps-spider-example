# -*- coding: utf-8 -*-
import os
import logging

THREAD_COUNT = 20
MONGO_DB = 'yandex'
TASK_FILE = os.path.join(os.path.dirname(__file__), 'example/tasks.csv')
RESULT_FILE = os.path.join(os.path.dirname(__file__), 'example/result.json')
LOG_LEVEL = logging.DEBUG

try:
    from local_settings import *
except ImportError:
    pass
