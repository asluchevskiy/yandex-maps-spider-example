# -*- coding: utf-8 -*-
import logging
from settings import *
from app import YandexMapsSpider, Exporter

logging.basicConfig(level=LOG_LEVEL)
YandexMapsSpider(thread_number=THREAD_COUNT).run()
Exporter().run()
