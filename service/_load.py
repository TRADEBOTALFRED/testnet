import decimal
import time

from service.models import *
from .markets import binance_api

from datetime import datetime, timedelta
from django.utils import timezone
import random
from service import data_loader

global available_to_download_per_time

t1 = int(time.time())
t0 = t1-365*24*60*60

for t in range(t0, t1, 5*60):
	global available_to_download_per_time
	available_to_download_per_time = 1
	data_loader.load_5m_for(t, True)