
from datetime import date
from django.utils.dateparse import parse_datetime
from timezonefinder import TimezoneFinder
from pytz import timezone
from app.models import Request
from datetime import datetime as dt

def parseStrDate(str_date,lat,lon):
    date_date=parse_datetime(str_date)

    rqGETTimeZone=Request.objects.get(name='getTimeZone')
    now = dt.now()
    timestamp = dt.timestamp(now)   
    strtimezone=rqGETTimeZone.executeFunction([str(lat)+','+str(lon),str(timestamp),rqGETTimeZone.RApi.APIKey])
   
    date_date=date_date.astimezone(timezone(strtimezone))
    return date_date
