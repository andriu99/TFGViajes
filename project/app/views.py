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

            end_date_local=form.cleaned_data['date']+datetime.timedelta(days=1)
            print(end_date_local)
            
            start_coordinates=str(form.cleaned_data['lat_Origin'])+','+str(form.cleaned_data['lon_Origin'])

            end_coordinates=str(form.cleaned_data['lat_Dest'])+','+str(form.cleaned_data['lon_Dest'])
            iterableBlablaCar=getBlablaCarTrips.executeFunction([getBlablaCarTrips.RApi.APIKey,start_coordinates,end_coordinates,'EUR',form.cleaned_data['date'].isoformat(),end_date_local])
            for a,b,c,d in iterableBlablaCar:
                print(a,b,c,d)
    else:
        form = userRequest()
    

    context = {'form' : form}
    return render(request,'app/home.html',context)