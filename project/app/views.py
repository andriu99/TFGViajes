#from project.app.models import blablaTrip
from django.shortcuts import render
from .forms import userRequest
from app.models import Request,Trip,blablaTrip,skyscannerTrip,Node
from datetime import datetime as dt
from datetime import timedelta
from .otherFunctions.dateFunctions import parseStrDate
from .otherFunctions.nodesFunctions import filterAirportsNodes


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
                startData_date = parseStrDate(startData_str,float(startData_latitude),float(startData_latitude)) 
                endData_date = parseStrDate(endData_str,float(endData_latitude),float(endData_longitude)) 
                
                diffDate=endData_date-startData_date
                duration=diffDate.seconds

                
             
                new_trip=Trip(departureDate=startData_date,arrivalDate=endData_date,duration=duration,price=float(price))
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

                        startData_date = parseStrDate(departure_date,float(startData_latitude),float(startData_latitude)) 
                        endData_date = parseStrDate(arrival_date,float(endData_latitude),float(endData_longitude))
                        new_trip=Trip(departureDate=startData_date,arrivalDate=endData_date,duration=duration,price=float(price))
                        new_trip.save()
                        print(airlineName)
                        new_skyscannerTrip=skyscannerTrip(urlPay=urlPay,airlineName=airlineName,airlineUrlImage=airlineUrlImage,trip=new_trip)
                        new_skyscannerTrip.save()

                    
            

    else:
        Trip.objects.all().delete()
        form = userRequest()
    
    blablaTrips=blablaTrip.objects.all()
    skyscannerTrips=skyscannerTrip.objects.all()
    context = {'form' : form,'blablaTrips':blablaTrips,'skyscannerTrips':skyscannerTrips}
    return render(request,'app/home.html',context)