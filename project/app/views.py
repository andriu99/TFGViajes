from django.shortcuts import render
from .forms import userRequest
from app.models import Request,Trip
import datetime


def home(request):
    if request.method == 'POST':
        form = userRequest(request.POST)
        if form.is_valid():
            Trip.objects.all().delete()
            getBlablaCarTrips=Request.objects.get(name='getBlablaCarTrips')
          
            originalDate=form.cleaned_data['date']
            start_date_local=datetime.datetime(originalDate.year,originalDate.month,originalDate.day)
            start_date_local_string=start_date_local.isoformat()

            end_date_local_string=(start_date_local+datetime.timedelta(days=1)).isoformat()
          
            start_coordinates=str(form.cleaned_data['lat_Origin'])+','+str(form.cleaned_data['lon_Origin'])

            end_coordinates=str(form.cleaned_data['lat_Dest'])+','+str(form.cleaned_data['lon_Dest'])
            iterableBlablaCar=getBlablaCarTrips.executeFunction([getBlablaCarTrips.RApi.APIKey,start_coordinates,end_coordinates,'EUR',start_date_local_string,end_date_local_string])
            for (url,
                 startData_str,startData_city,startData_address,startData_latitude,startData_longitude,
                 endData_str,endDatacity,endDataaddress,endDatalatitude,endDatalongitude,
                 price
            ) in iterableBlablaCar:
                startData_date = datetime.datetime.strptime(startData_str, '%Y-%m-%dT%H:%M:%S')
                endData_date = datetime.datetime.strptime(endData_str, '%Y-%m-%dT%H:%M:%S')

                diffDate=endData_date-startData_date
                duration=diffDate.seconds
                print(duration)
                print(price)
                print(type(price))
                #new_trip=Trip(departureDate=startData_date,arrivalDate=endData_date,duration=duration,price=)


                # print(url)
                # print(startData_date,startData_city,startData_address,startData_latitude,startData_longitude)
                # print(endData_date,endDatacity,endDataaddress,endDatalatitude,endDatalongitude)
                # print(price)
    else:
        form = userRequest()
    

    context = {'form' : form}
    return render(request,'app/home.html',context)