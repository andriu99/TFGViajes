#from project.app.models import blablaTrip
#from project.app.models import busOrTrainTrip
from django.shortcuts import render
from .forms import userRequest
from app.models import Trip,blablaTrip,skyscannerTrip,busOrTrainTrip,RESTApi
import googlemaps
from datetime import datetime as dt 
from .viewFunctions.homeviewFunctions import saveBlablacarTrips,saveSkyscannerFlights,save_train_bus_trips
from .funtionsRequest.googleMapsRequests import getLatLong_address


def home(request):
    Trip.objects.all().delete()

    if request.method == 'POST':
        form = userRequest(request.POST)
        if form.is_valid():

            print(form.cleaned_data)
            originalDate=form.cleaned_data['date']
            start_date_local=dt(originalDate.year,originalDate.month,originalDate.day)

            start_coordinates=str(form.cleaned_data['lat_Origin'])+','+str(form.cleaned_data['lon_Origin'])
            end_coordinates=str(form.cleaned_data['lat_Dest'])+','+str(form.cleaned_data['lon_Dest'])


            #saveBlablacarTrips(start_coordinates,end_coordinates,start_date_local)
            #saveSkyscannerFlights(start_coordinates,end_coordinates,start_date_local)
            save_train_bus_trips(start_coordinates,end_coordinates,start_date_local)


    else:

        form = userRequest()

    
    blablaTrips=blablaTrip.objects.all()
    skyscannerTrips=skyscannerTrip.objects.all()
    try:
        busTrips=busOrTrainTrip.objects.filter(system='B')
    except:
        busTrips={}

    try:
        trainTrips=busOrTrainTrip.objects.filter(system='T')
    except:
        trainTrips={}

    context = {'form' : form,'blablaTrips':blablaTrips,'skyscannerTrips':skyscannerTrips,'busTrips':busTrips,'trainTrips':trainTrips}
    return render(request,'app/home.html',context)


def new(request):
    return render(request,'app/new.html')