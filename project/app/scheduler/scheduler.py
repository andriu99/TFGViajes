from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys
from ..models import Trip 
from datetime import datetime as dt 
#from django.utils import timezone
from datetime import timezone
from ..otherFunctions.dateFunctions import is_old_date

def myfunc():
    set_TripID_toDelete=set()
    for trip in Trip.objects.all():
    
        if (hasattr(trip,"blablaTrip")):
            lat=trip.blablaTrip.latitude
            lng=trip.blablaTrip.longitude

        else:
            lat=trip.arrivalNode.latitude
            lng=trip.arrivalNode.longitude

        is_old_trip=is_old_date(trip.arrivalDate,lat,lng)
        if is_old_trip:
            set_TripID_toDelete.add(trip.pk)

    #Trip.objects.filter(id__in=set_TripID_toDelete).delete()
       

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(myfunc, 'interval', seconds=60)
    scheduler.start()

