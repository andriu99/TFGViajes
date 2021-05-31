from re import search
from app.models import Request,Trip,blablaTrip,skyscannerTrip,busOrTrainTrip,RESTApi
from datetime import timedelta, tzinfo
from ..otherFunctions.dateFunctions import parseDate_withTimeZone,calculateDuration
from ..otherFunctions.nodesFunctions import filterNodes
from django.utils.dateparse import parse_datetime
import googlemaps as gmaps
from ..funtionsRequest.googleMapsRequests import getProvinceLocationThroughCoordinates


def saveBlablacarTrips(start_coordinates,end_coordinates,start_date_local):
    set_trips_blabla=set()
    getBlablaCarTrips=Request.objects.get(name='getBlablaCarTrips')

    end_date_local_string=(start_date_local+timedelta(days=1)).isoformat()
    

    iterableBlablaCar=getBlablaCarTrips.executeFunction([getBlablaCarTrips.RApi.APIKey,start_coordinates,end_coordinates,'EUR',start_date_local.isoformat(),end_date_local_string])
    for (   url,
            startData_str,startData_city,startData_address,startData_latitude,startData_longitude,
            endData_str,endData_city,endData_address,endData_latitude,endData_longitude,
            price

    ) in iterableBlablaCar:

        departureDate_date=parse_datetime(startData_str)
        arrivalDate_date=parse_datetime(endData_str)

        startData_date_withTimeZone = parseDate_withTimeZone(departureDate_date,startData_latitude,startData_longitude) 
        endData_date_withTimeZone = parseDate_withTimeZone(arrivalDate_date,endData_latitude,endData_longitude)

        duration=calculateDuration(startData_date_withTimeZone,endData_date_withTimeZone)

        

        
        new_trip=Trip(departureNode=None,arrivalNode=None,departureDate=departureDate_date,arrivalDate=arrivalDate_date,duration=duration.seconds,price=float(price))
        new_trip.save()
        set_trips_blabla.add(new_trip.pk)



        new_blablatrip=blablaTrip(link=url,
                                    departureCity=startData_city,departureAddress=startData_address,departureLatitude=float(startData_latitude),departureLongitude=float(startData_longitude),
                                    arrivalCity=endData_city,arrivalAddress=endData_address,arrivalLatitude=float(endData_latitude),arrivalLongitude=float(endData_longitude),
                                    trip=new_trip

        )
        new_blablatrip.save()

        return Trip.objects.filter(id__in=set_trips_blabla)


def saveSkyscannerFlights(start_coordinates,end_coordinates,start_date_local):
    set_trips_skys=set()
    getskyscannerTrips=Request.objects.get(name='getTokenSkyscanner')
    token=getskyscannerTrips.executeFunction([getskyscannerTrips.RApi.APIKey])

    getSessionKeySkyscanner=Request.objects.get(name='getSessionKeySkyscanner')
    getFlightsInformationSkyscanner=Request.objects.get(name='getFlightsInformationSkyscanner')
    
    outboundDate='{y}-{m}-{d}'.format(y=str(start_date_local.year),m=str(start_date_local.month).zfill(2),d=str(start_date_local.day).zfill(2))
    
    filter_DepartureNodes=filterNodes(start_coordinates)
    filter_ArrivalNodes=filterNodes(end_coordinates)
    for departureNode in filter_DepartureNodes:
        for arrivalNode in filter_ArrivalNodes:
            paramsList=['Economy','ES','EUR','es-ES','iata',departureNode.code,arrivalNode.code,outboundDate,1,0,0,token]
            SessionKey=getSessionKeySkyscanner.executeFunction(paramsList)
            getFlightsInformationSkyscanner.PartToaddToBaseUrl+=SessionKey
            results=getFlightsInformationSkyscanner.executeFunction([0,token])


            urlList=(getFlightsInformationSkyscanner.PartToaddToBaseUrl.split('/'))
            urlList.pop()
            getFlightsInformationSkyscanner.PartToaddToBaseUrl="/".join(urlList)


            for price,urlPay,departure_date_str,arrival_date_str,duration,airlineName,airlineUrlImage in results:
                startData_date = parse_datetime(departure_date_str)
                endData_date = parse_datetime(arrival_date_str)
                

                new_trip=Trip(departureNode=departureNode,arrivalNode=arrivalNode,departureDate=startData_date,arrivalDate=endData_date,duration=duration*60,price=float(price))
                new_trip.save()
                set_trips_skys.add(new_trip.pk)
                new_skyscannerTrip=skyscannerTrip(urlPay=urlPay,airlineName=airlineName,airlineUrlImage=airlineUrlImage,trip=new_trip)
                new_skyscannerTrip.save()

    return Trip.objects.filter(id__in=set_trips_skys)


'''
Guardo los viajes en la BD, y además los incluyo en un array para saber cuáles han sido los últimos guardados.
'''
def save_tripsInfo_DepArriNodes(filter_departureNodes,filter_arrivalNodes,start_date_local,getBusTrainTrips,set_bustrain_Trips=None):
    
    for departureNode in filter_departureNodes:
        for arrivalNode in filter_arrivalNodes:
            save_busTrainTrip(departureNode,arrivalNode,start_date_local,getBusTrainTrips,set_bustrain_Trips)

            #print(departureNode.name+'  '+arrivalNode.name)
            # searchDict['departure_station_id']=int(departureNode.code)
            # searchDict['arrival_station_id']=int(arrivalNode.code)
            # searchDict['departure_date']=start_date_local.isoformat()

            # for system in system_transport_dict:
            #     searchDict['systems']=system_transport_dict[system]
            #     tripGenerator=getBusTrainTrips.executeFunction(['EUR',searchDict],typeOfData='str')

            #     if tripGenerator!=None:
            #         for price,departureDate_str,arrivalDate_str in tripGenerator:
            #             departureDate_date=parse_datetime(departureDate_str)
            #             arrivalDate_date=parse_datetime(arrivalDate_str)

            #             departureDate_withTimeZone = parseDate_withTimeZone(departureDate_date,departureNode.latitude,departureNode.longitude)
            #             arrivalDate_withTimeZone = parseDate_withTimeZone(arrivalDate_date,arrivalNode.latitude,arrivalNode.longitude)
                    
            #             duration=calculateDuration(departureDate_withTimeZone,arrivalDate_withTimeZone)

            #             new_trip=Trip(departureNode=departureNode,arrivalNode=arrivalNode,departureDate=departureDate_date.replace(tzinfo=None),arrivalDate=arrivalDate_date.replace(tzinfo=None),duration=duration.seconds,price=price)
            #             new_trip.save()
                        
            #             bus_train_trip=busOrTrainTrip(system=system,trip=new_trip)
            #             bus_train_trip.save()
            #             if set_bustrain_Trips!=None:
            #                 set_bustrain_Trips.add(new_trip.pk)
                        
                        
def save_busTrainTrip(departureNode,arrivalNode,start_date_local,getBusTrainTrips,set_bustrain_Trips=None):
    searchDict=get_SearchDict()

    searchDict['departure_station_id']=int(departureNode.code)
    searchDict['arrival_station_id']=int(arrivalNode.code)
    searchDict['departure_date']=start_date_local.isoformat()

    system_transport_dict=get_systemOfTransport_dict()
    for system in system_transport_dict:
        searchDict['systems']=system_transport_dict[system]
        tripGenerator=getBusTrainTrips.executeFunction(['EUR',searchDict],typeOfData='str')

        if tripGenerator!=None:
            for price,departureDate_str,arrivalDate_str in tripGenerator:

                departureDate_date=parse_datetime(departureDate_str)

                if (departureDate_date.replace(tzinfo=None)<(start_date_local+timedelta(days=1))):
                    arrivalDate_date=parse_datetime(arrivalDate_str)

                    departureDate_withTimeZone = parseDate_withTimeZone(departureDate_date,departureNode.latitude,departureNode.longitude)
                
                    arrivalDate_withTimeZone = parseDate_withTimeZone(arrivalDate_date,arrivalNode.latitude,arrivalNode.longitude)
                
                    duration=calculateDuration(departureDate_withTimeZone,arrivalDate_withTimeZone)

                    new_trip=Trip(departureNode=departureNode,arrivalNode=arrivalNode,departureDate=departureDate_date.replace(tzinfo=None),arrivalDate=arrivalDate_date.replace(tzinfo=None),duration=duration.seconds,price=price)
                    new_trip.save()
                    
                    bus_train_trip=busOrTrainTrip(system=system,trip=new_trip)
                    bus_train_trip.save()
                    if set_bustrain_Trips!=None:
                        set_bustrain_Trips.add(new_trip.pk)





def get_SearchDict():

    searchDict={
            "passenger_ids": [
            "314892886"
            ],
            "card_ids": [
            "14127110"
            ],
            "departure_station_id":0,
            "arrival_station_id":0,
            "departure_date":"2021-03-29T00:00:00+01:00",
            "systems":[]
        }

    return searchDict

def get_systemOfTransport_dict():

    return {
        'T':['renfe'],
        'B':['busbud']
    }

def get_locat_province(coordinates):
    
    ClientGMaps=gmaps.Client(RESTApi.objects.get(name='googleMapsRESTApi').APIKey)
    location,province=getProvinceLocationThroughCoordinates(ClientGMaps.reverse_geocode(coordinates))
    return location,province



def save_train_bus_trips(start_coordinates,end_coordinates,start_date_local):
    print(type(start_date_local))

    locatO,provO=get_locat_province(start_coordinates)
    locatD,provD=get_locat_province(end_coordinates)

    filter_departureNodes=filterNodes(start_coordinates,nodeType='S')
    filter_arrivalNodes=filterNodes(end_coordinates,nodeType='S')
    

  
    set_bustrain_Trips=set()
    for bus_trainTrip in busOrTrainTrip.objects.all():
        actual_trip=bus_trainTrip.trip

        if (actual_trip.departureDate>=start_date_local and actual_trip.departureDate<=(start_date_local+timedelta(days=1))):
            if(actual_trip.departureNode.location==locatO and actual_trip.arrivalNode.location==locatD):
                set_bustrain_Trips.add(actual_trip.pk)
        
    if not set_bustrain_Trips: 
        getBusTrainTrips=Request.objects.get(name='getbustrainTripsInformationTrainline')
        
      
        save_tripsInfo_DepArriNodes(filter_departureNodes,filter_arrivalNodes,start_date_local,getBusTrainTrips,set_bustrain_Trips)
    
    query_set_bustrain_Trips=Trip.objects.filter(id__in=set_bustrain_Trips)
    return query_set_bustrain_Trips
    


