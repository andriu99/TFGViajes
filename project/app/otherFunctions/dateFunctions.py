
from datetime import date
from django.utils.dateparse import parse_datetime
from pytz import timezone
from app.models import Request
from datetime import datetime as dt
from datetime import timedelta
import pytz

def parseStrDate(str_date,lat,lon):
    date_date=parse_datetime(str_date)

    rqGETTimeZone=Request.objects.get(name='getTimeZone')
    now = dt.now()
    timestamp = dt.timestamp(now)   
    strtimezone=rqGETTimeZone.executeFunction([str(lat)+','+str(lon),str(timestamp),rqGETTimeZone.RApi.APIKey])
    #pytz.timezone(strtimezone).localize(date_date, is_dst=None)
    date_date=date_date.astimezone(timezone(strtimezone))
    print(date_date.tzinfo)
    return date_date


def calculateDuration(startData_date,endData_date):
    difHours_departure_withUT0=int(startData_date.isoformat()[-6]+startData_date.isoformat()[-4]) #diference between 00:00 time zone and departure time zone
    difHours_arrival_withUT0=int(startData_date.isoformat()[-6]+endData_date.isoformat()[-4])
    
    difHours_arrival_departure=difHours_arrival_withUT0-difHours_departure_withUT0

    duration=endData_date-startData_date
    duration=duration+timedelta(hours=(-1)*difHours_arrival_departure)
    return duration