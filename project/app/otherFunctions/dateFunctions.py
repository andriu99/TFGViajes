
from datetime import date
from django.utils.dateparse import parse_datetime
from timezonefinder import TimezoneFinder
from pytz import timezone

def parseStrDate(str_date,lat,lon):
    date_date=parse_datetime(str_date)
    tf = TimezoneFinder()
    time_zone=tf.timezone_at(lng=lon, lat=lat)
  
    date_date=date_date.astimezone(timezone(time_zone))
    return date_date
