
from datetime import datetime as dt
from datetime import timedelta
import pytz
from datetime import timezone as tz
from ..funtionsRequest.googleMapsRequests import parseDate_withTimeZone



def calculateDuration(startData_date,endData_date):
    difHours_departure_withUT0=int(startData_date.isoformat()[-6]+startData_date.isoformat()[-4]) #diference between 00:00 time zone and departure time zone
    difHours_arrival_withUT0=int(startData_date.isoformat()[-6]+endData_date.isoformat()[-4])
    
    difHours_arrival_departure=difHours_arrival_withUT0-difHours_departure_withUT0

    duration=endData_date-startData_date
    duration=duration+timedelta(hours=(-1)*difHours_arrival_departure)
    return duration


def is_old_date(date,lat,lon):
    now = dt.now(tz.utc)
    data_with_TimeZone=parseDate_withTimeZone(date,lat,lon)
    
    difHours_arrival_withUT0=int(data_with_TimeZone.isoformat()[-6]+data_with_TimeZone.isoformat()[-4]) #diference between 00:00 time zone and departure time zone
    date_withoutTZ=date+timedelta(hours=(-1)*difHours_arrival_withUT0)
    timezone_UT0 = pytz.timezone("UTC")
    date_UTC0 = timezone_UT0.localize(date_withoutTZ)

    
    return now>=date_UTC0







