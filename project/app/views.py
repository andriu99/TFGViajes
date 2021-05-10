from django.shortcuts import render
from .forms import userRequest
from app.models import Request,RESTApi,Node
import datetime

def home(request):
    if request.method == 'POST':
        form = userRequest(request.POST)
        if form.is_valid():
            getBlablaCarTrips=Request.objects.get(name='getBlablaCarTrips')
            # print(form.cleaned_data['date'])
            # print(form.cleaned_data['date']+datetime.timedelta(days=1))
            originalDate=form.cleaned_data['date']
            start_date_local=datetime.datetime(originalDate.year,originalDate.month,originalDate.day)
            start_date_local_string=start_date_local.isoformat()

            end_date_local_string=(start_date_local+datetime.timedelta(days=1)).isoformat()
          
            start_coordinates=str(form.cleaned_data['lat_Origin'])+','+str(form.cleaned_data['lon_Origin'])

            end_coordinates=str(form.cleaned_data['lat_Dest'])+','+str(form.cleaned_data['lon_Dest'])
            iterableBlablaCar=getBlablaCarTrips.executeFunction([getBlablaCarTrips.RApi.APIKey,start_coordinates,end_coordinates,'EUR',start_date_local_string,end_date_local_string])
            for (url,
                 startData_date,startData_city,startData_address,startData_latitude,startData_longitude,
                 endDatadate,endDatacity,endDataaddress,endDatalatitude,endDatalongitude,
                 price
            ) in iterableBlablaCar:
                print(url)
                print(startData_date,startData_city,startData_address,startData_latitude,startData_longitude)
                print(endDatadate,endDatacity,endDataaddress,endDatalatitude,endDatalongitude)
                print(price)
    else:
        form = userRequest()
    

    context = {'form' : form}
    return render(request,'app/home.html',context)