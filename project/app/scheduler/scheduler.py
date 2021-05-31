from apscheduler.schedulers.background import BackgroundScheduler
from ..models import Trip 
from ..otherFunctions.dateFunctions import is_old_date
from app.models import Request,Trip
from ..viewFunctions.homeviewFunctions import save_busTrainTrip


def update_trips():
    trip_set=set()

    for trip in Trip.objects.all():
        if (hasattr(trip,"blablaTrip")):
            lat=trip.blablaTrip.latitude
            lng=trip.blablaTrip.longitude

        else:
            lat=trip.arrivalNode.latitude
            lng=trip.arrivalNode.longitude

        is_old_trip=is_old_date(trip.arrivalDate,lat,lng)

        if is_old_trip:
            trip.delete()
        
        else:
            if (hasattr(trip,"busOrTrainTrip")):
                trip_set.add(Trip.objects.all().filter(departureNode=trip.departureNode,arrivalNode=trip.arrivalNode))




    for queryset in trip_set:
        '''
        Evaluo sólo el primer viaje del queryset ya que tiene las mismas estaciones de origen y destino que el resto de viajes
        Reseteo esos viajes
        '''
        trip0=queryset[0]
        departureDate=trip0.departureDate.replace(hour=0).replace(minute=0).replace(second=0)
        getBusTrainTrips=Request.objects.get(name='getbustrainTripsInformationTrainline')

        save_busTrainTrip(trip0.departureNode,trip0.arrivalNode,departureDate,getBusTrainTrips) 


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_trips, 'interval', seconds=360)
    scheduler.start()

