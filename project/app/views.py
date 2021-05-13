#from project.app.models import blablaTrip
from django.shortcuts import render
from .forms import userRequest
from app.models import Request,Trip,blablaTrip,skyscannerTrip,Node
from datetime import datetime as dt
from datetime import timedelta
from .otherFunctions.dateFunctions import parseStrDate
from .otherFunctions.nodesFunctions import filterAirportsNodes

import pytz


def home(request):
    if request.method == 'POST':
        Trip.objects.all().delete()
        form = userRequest(request.POST)
        if form.is_valid():
            getBlablaCarTrips=Request.objects.get(name='getBlablaCarTrips')
          
            originalDate=form.cleaned_data['date']
            start_date_local=dt(originalDate.year,originalDate.month,originalDate.day)
            start_date_local_string=start_date_local.isoformat()

            end_date_local_string=(start_date_local+timedelta(days=1)).isoformat()
          
            start_coordinates=str(form.cleaned_data['lat_Origin'])+','+str(form.cleaned_data['lon_Origin'])

            end_coordinates=str(form.cleaned_data['lat_Dest'])+','+str(form.cleaned_data['lon_Dest'])
            iterableBlablaCar=getBlablaCarTrips.executeFunction([getBlablaCarTrips.RApi.APIKey,start_coordinates,end_coordinates,'EUR',start_date_local_string,end_date_local_string])
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






            # getBusTrainTrips=Request.objects.get(name='getbustrainTripsInformationTrainline')
            # searchDict={
            #     "passenger_ids": [
            #     "314892886"
            #     ],
            #     "card_ids": [
            #     "14127110"
            #     ],
            #     "departure_station_id":0,
            #     "arrival_station_id":0,
            #     "departure_date":"2021-03-29T00:00:00+01:00",
            #     "systems":[]
            # }
            # filter_departureNodes=filterAirportsNodes(start_coordinates,nodeType='S')
            # filter_arrivalNodes=filterAirportsNodes(end_coordinates,nodeType='S')

            # for departureNode in filter_departureNodes:
            #     for arrivalNode in filter_arrivalNodes:
            #         searchDict['departure_station_id']=int(departureNode.code)
            #         searchDict['arrival_station_id']=int(arrivalNode.code)
            #         searchDict['departure_date']=start_date_local_string
            #         searchDict['systems']=['renfe']
            #         tripGenerator=getBusTrainTrips.executeFunction(['EUR',searchDict],typeOfData='str')
            #         # print(departureNode.code)
            #         # print(arrivalNode.code)

            #         #print(a)
            #         if tripGenerator!=None:
            #             for price,departureDate,arrivalDate in tripGenerator:
            #                 print(price,departure_date,arrivalDate)
                

    else:
        Trip.objects.all().delete()
        form = userRequest()
    
    blablaTrips=blablaTrip.objects.all()
    skyscannerTrips=skyscannerTrip.objects.all()
    context = {'form' : form,'blablaTrips':blablaTrips,'skyscannerTrips':skyscannerTrips}
    return render(request,'app/home.html',context)