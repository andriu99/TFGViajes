#from project.app.models import blablaTrip
from django.shortcuts import render
from .forms import userRequest
from app.models import Request,Trip,blablaTrip,skyscannerTrip,Node
from datetime import datetime as dt
from datetime import timedelta
from .otherFunctions.dateFunctions import parseStrDate
from .otherFunctions.nodesFunctions import filterAirportsNodes

from .viewFunctions.homeviewFunctions import saveBlablacarTrips,saveSkyscannerFlights,save_train_bus_trips

import pytz


def home(request):
    if request.method == 'POST':
        Trip.objects.all().delete()
        form = userRequest(request.POST)
        if form.is_valid():


            originalDate=form.cleaned_data['date']
            start_date_local=dt(originalDate.year,originalDate.month,originalDate.day)

            start_coordinates=str(form.cleaned_data['lat_Origin'])+','+str(form.cleaned_data['lon_Origin'])
            end_coordinates=str(form.cleaned_data['lat_Dest'])+','+str(form.cleaned_data['lon_Dest'])


            saveBlablacarTrips(start_coordinates,end_coordinates,start_date_local)
            saveSkyscannerFlights(start_coordinates,end_coordinates,start_date_local)
            save_train_bus_trips(start_coordinates,end_coordinates,start_date_local)


    else:
        Trip.objects.all().delete()
        form = userRequest()
    
    blablaTrips=blablaTrip.objects.all()
    skyscannerTrips=skyscannerTrip.objects.all()
    context = {'form' : form,'blablaTrips':blablaTrips,'skyscannerTrips':skyscannerTrips}
    return render(request,'app/home.html',context)