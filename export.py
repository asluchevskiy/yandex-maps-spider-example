# -*- coding: utf-8 -*-
import sys
import locale
import logging
from settings import *
from app import Exporter

reload(sys)
sys.setdefaultencoding(locale.getpreferredencoding())
logging.basicConfig(level=LOG_LEVEL)
Exporter().export_json()
