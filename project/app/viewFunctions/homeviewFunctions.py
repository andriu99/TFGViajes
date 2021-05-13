from app.models import Request,Trip,blablaTrip,skyscannerTrip
from datetime import datetime as dt
from datetime import timedelta
from ..otherFunctions.dateFunctions import parseStrDate
from ..otherFunctions.nodesFunctions import filterAirportsNodes

def saveBlablacarTrips(start_coordinates,end_coordinates,start_date_local):
    getBlablaCarTrips=Request.objects.get(name='getBlablaCarTrips')

    end_date_local_string=(start_date_local+timedelta(days=1)).isoformat()
    

    iterableBlablaCar=getBlablaCarTrips.executeFunction([getBlablaCarTrips.RApi.APIKey,start_coordinates,end_coordinates,'EUR',start_date_local.isoformat(),end_date_local_string])
    for (url,
            startData_str,startData_city,startData_address,startData_latitude,startData_longitude,
            endData_str,endData_city,endData_address,endData_latitude,endData_longitude,
            price

    ) in iterableBlablaCar:

        startData_date = parseStrDate(startData_str,startData_latitude,startData_longitude) 
        endData_date = parseStrDate(endData_str,endData_latitude,endData_longitude)

        
        difHours_departure_withUT0=int(startData_date.isoformat()[-6]+startData_date.isoformat()[-4]) #diference between 00:00 time zone and departure time zone
        difHours_arrival_withUT0=int(startData_date.isoformat()[-6]+endData_date.isoformat()[-4])
        
        difHours_arrival_departure=difHours_arrival_withUT0-difHours_departure_withUT0

        duration=endData_date-startData_date
        duration=duration+timedelta(hours=(-1)*difHours_arrival_departure)
        
        
        new_trip=Trip(departureDate=startData_date,arrivalDate=endData_date,duration=duration.seconds,price=float(price))
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
    
    filter_DepartureNodes=filterAirportsNodes(start_coordinates)
    filter_ArrivalNodes=filterAirportsNodes(end_coordinates)
    for departureNode in filter_DepartureNodes:
        for arrivalNode in filter_ArrivalNodes:
            paramsList=['Economy','ES','EUR','es-ES','iata',departureNode.code,arrivalNode.code,outboundDate,1,0,0,token]
            SessionKey=getSessionKeySkyscanner.executeFunction(paramsList)
            getFlightsInformationSkyscanner.PartToaddToBaseUrl+=SessionKey
            results=getFlightsInformationSkyscanner.executeFunction([0,token])


            urlList=(getFlightsInformationSkyscanner.PartToaddToBaseUrl.split('/'))
            urlList.pop()
            getFlightsInformationSkyscanner.PartToaddToBaseUrl="/".join(urlList)


            for price,urlPay,departure_date,arrival_date,duration,airlineName,airlineUrlImage in results:
                startData_date = parseStrDate(departure_date,departureNode.latitude,departureNode.longitude)
                endData_date = parseStrDate(arrival_date,arrivalNode.latitude,arrivalNode.longitude)
                

                new_trip=Trip(departureDate=startData_date,arrivalDate=endData_date,duration=duration*60,price=float(price))
                new_trip.save()
                new_skyscannerTrip=skyscannerTrip(urlPay=urlPay,airlineName=airlineName,airlineUrlImage=airlineUrlImage,trip=new_trip)
                new_skyscannerTrip.save()


def save_train_bus_trips(start_coordinates,end_coordinates,start_date_local):
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
    filter_departureNodes=filterAirportsNodes(start_coordinates,nodeType='S')
    filter_arrivalNodes=filterAirportsNodes(end_coordinates,nodeType='S')

    for departureNode in filter_departureNodes:
        for arrivalNode in filter_arrivalNodes:
            searchDict['departure_station_id']=int(departureNode.code)
            searchDict['arrival_station_id']=int(arrivalNode.code)
            searchDict['departure_date']=start_date_local.isoformat()
            searchDict['systems']=['renfe']
            tripGenerator=getBusTrainTrips.executeFunction(['EUR',searchDict],typeOfData='str')
            
            if tripGenerator!=None:
                for price,departureDate,arrivalDate in tripGenerator:
                    print(price,departureDate,arrivalDate)


