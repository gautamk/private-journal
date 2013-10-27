from datetime import datetime
from pretty_timedelta import pretty_timedelta

__author__ = 'gautam'

def pretty_time(datetime_value):
    now = datetime.now()
    delta = datetime_value -  now
    return pretty_timedelta(delta)
