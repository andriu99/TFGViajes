
from django.shortcuts import render
from .forms import userRequest
from app.models import blablaTrip,skyscannerTrip,Trip
import googlemaps
from datetime import datetime as dt 
from .viewFunctions.homeviewFunctions import saveBlablacarTrips,saveSkyscannerFlights,save_train_bus_trips
from .funtionsRequest.googleMapsRequests import getLatLong_address


def home(request):
    #Trip.objects.all().delete()
    for trip in Trip.objects.all():
        try:
            trip.busOrTrainTrip

        except:
            Trip.objects.all().delete(pk=trip.pk)

    blablaTrip.objects.all().delete()
    skyscannerTrip.objects.all().delete()
    if request.method == 'POST':
        form = userRequest(request.POST)
        if form.is_valid():


            date=form.cleaned_data['date']
            start_date_local=dt(date.year,date.month,date.day)
            print(date)
            print(type(date))

            start_coordinates=str(form.cleaned_data['lat_Origin'])+','+str(form.cleaned_data['lon_Origin'])
            end_coordinates=str(form.cleaned_data['lat_Dest'])+','+str(form.cleaned_data['lon_Dest'])


            saveBlablacarTrips(start_coordinates,end_coordinates,start_date_local)
            saveSkyscannerFlights(start_coordinates,end_coordinates,start_date_local)
            query_set_bustrain_Trips=save_train_bus_trips(start_coordinates,end_coordinates,start_date_local)

    else:

        form = userRequest()

    
    blablaTrips=blablaTrip.objects.all()
    skyscannerTrips=skyscannerTrip.objects.all()

    

    try:
        busTrips=query_set_bustrain_Trips.filter(system='B')
    except:
        busTrips={}

    try:
        trainTrips=query_set_bustrain_Trips.filter(system='T')
    except:
        trainTrips={}




    context = {'form' : form,'blablaTrips':blablaTrips,'skyscannerTrips':skyscannerTrips,'busTrips':busTrips,'trainTrips':trainTrips}
    return render(request,'app/home.html',context)


def new(request):
    return render(request,'app/new.html')