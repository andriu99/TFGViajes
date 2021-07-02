from apscheduler.schedulers.background import BackgroundScheduler
from ..models import Trip,Request,Node
from ..otherFunctions.dateFunctions import is_old_date
from ..viewFunctions.homeviewFunctions import save_busTrainTrip


def update_trips():
    trip_list=list()
    list_combinations=list()
    

    for trip in Trip.objects.all():

        if (hasattr(trip,"blablaTrip")):
            lat=trip.blablaTrip.arrivalLatitude
            lng=trip.blablaTrip.arrivalLongitude

        else:
            lat=trip.arrivalNode.latitude
            lng=trip.arrivalNode.longitude

        is_old_trip=is_old_date(trip.arrivalDate,lat,lng)

        if is_old_trip:
            trip.delete()
        
        else:
            if (hasattr(trip,"busOrTrainTrip")):
                combination=[trip.departureNode.code,trip.arrivalNode.code,trip.departureDate.year,trip.departureDate.month,trip.departureDate.day]
                if combination not in list_combinations:
                    list_combinations.append(combination)
                    query_set_trips=Trip.objects.all().filter(departureNode=trip.departureNode).filter(arrivalNode=trip.arrivalNode).filter(departureDate__year=trip.departureDate.year,departureDate__month=trip.departureDate.month,departureDate__day=trip.departureDate.day)
                    trip_list.append(query_set_trips)


    ids_trip_to_remove=set()
    for queryset in trip_list:
    #     '''
    #     Evaluo sólo el primer viaje del queryset ya que tiene las mismas estaciones de origen y destino que el resto de viajes
    #     Reseteo esos viajes
    #     '''

        if queryset.exists():

            

            trip0=queryset.first()
           
            departureDate=trip0.departureDate.replace(hour=0).replace(minute=0).replace(second=0)
            getBusTrainTrips=Request.objects.get(name='getbustrainTripsInformationTrainline')

            for trip_remove in queryset:
                ids_trip_to_remove.add(trip_remove.pk)
            
            save_busTrainTrip(trip0.departureNode,trip0.arrivalNode,departureDate,getBusTrainTrips)

       

    
    trips_to_remove=Trip.objects.filter(id__in=ids_trip_to_remove)
    if set(Trip.objects.all()) !=set(trips_to_remove):
        trips_to_remove.delete()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_trips, 'interval', hours=24)
    scheduler.start()
