from app.models import Request,Trip,blablaTrip,skyscannerTrip,busOrTrainTrip,RESTApi
from datetime import datetime as dt
from datetime import timedelta
from ..otherFunctions.dateFunctions import parseDate_withTimeZone,calculateDuration
from ..otherFunctions.nodesFunctions import filterNodes
from django.utils.dateparse import parse_datetime
import googlemaps as gmaps
from ..funtionsRequest.googleMapsRequests import getProvinceLocationThroughCoordinates


def saveBlablacarTrips(start_coordinates,end_coordinates,start_date_local):
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

        new_blablatrip=blablaTrip(link=url,
                                    departureCity=startData_city,departureAddress=startData_address,departureLatitude=float(startData_latitude),departureLongitude=float(startData_longitude),
                                    arrivalCity=endData_city,arrivalAddress=endData_address,arrivalLatitude=float(endData_latitude),arrivalLongitude=float(endData_longitude),
                                    trip=new_trip

        )
        new_blablatrip.save()


def saveSkyscannerFlights(start_coordinates,end_coordinates,start_date_local):
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
                new_skyscannerTrip=skyscannerTrip(urlPay=urlPay,airlineName=airlineName,airlineUrlImage=airlineUrlImage,trip=new_trip)
                new_skyscannerTrip.save()


def save_tripInfo(searchDict,system_transport_dict,filter_departureNodes,filter_arrivalNodes,start_date_local,getBusTrainTrips):
           
    for departureNode in filter_departureNodes:
        for arrivalNode in filter_arrivalNodes:
            #print(departureNode.name+'  '+arrivalNode.name)
            searchDict['departure_station_id']=int(departureNode.code)
            searchDict['arrival_station_id']=int(arrivalNode.code)
            searchDict['departure_date']=start_date_local.isoformat()

            for system in system_transport_dict:
                searchDict['systems']=system_transport_dict[system]
                tripGenerator=getBusTrainTrips.executeFunction(['EUR',searchDict],typeOfData='str')

                if tripGenerator!=None:
                    for price,departureDate_str,arrivalDate_str in tripGenerator:
                        departureDate_date=parse_datetime(departureDate_str)
                        arrivalDate_date=parse_datetime(arrivalDate_str)

                        departureDate_withTimeZone = parseDate_withTimeZone(departureDate_date,departureNode.latitude,departureNode.longitude)
                        arrivalDate_withTimeZone = parseDate_withTimeZone(arrivalDate_date,arrivalNode.latitude,arrivalNode.longitude)
                    
                        duration=calculateDuration(departureDate_withTimeZone,arrivalDate_withTimeZone)

                        new_trip=Trip(departureNode=departureNode,arrivalNode=arrivalNode,departureDate=departureDate_date.replace(tzinfo=None),arrivalDate=arrivalDate_date.replace(tzinfo=None),duration=duration.seconds,price=price)
                        new_trip.save()
                        
                        bus_trains_trips=busOrTrainTrip(system=system,trip=new_trip)
                        bus_trains_trips.save()


def save_train_bus_trips(start_coordinates,end_coordinates,start_date_local):
    getskyscannerTrips=Request.objects.get(name='getTokenSkyscanner')
    ClientGMaps=gmaps.Client(RESTApi.objects.get(name='googleMapsRESTApi').APIKey)
    location,province=getProvinceLocationThroughCoordinates(ClientGMaps.reverse_geocode(start_coordinates))
    print(location,province)

    filter_departureNodes=filterNodes(start_coordinates,nodeType='S')
    filter_arrivalNodes=filterNodes(end_coordinates,nodeType='S')

    for bus_trainTrip in busOrTrainTrip.objects.all():
        actual_trip=bus_trainTrip.trip
        print(actual_trip.departureNode.location)
        print(actual_trip.arrivalNode.location)

    getBusTrainTrips=Request.objects.get(name='getbustrainTripsInformationTrainline')
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
    
    system_transport={
                'T':['renfe'],
                'B':['busbud']
    }
    #save_tripInfo(searchDict,system_transport,filter_departureNodes,filter_arrivalNodes,start_date_local,getBusTrainTrips)
 


