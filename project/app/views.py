#from project.app.models import blablaTrip
#from project.app.models import busOrTrainTrip
from django.shortcuts import render
from .forms import userRequest
from app.models import Trip,blablaTrip,skyscannerTrip,busOrTrainTrip,Request
import googlemaps

from .viewFunctions.homeviewFunctions import saveBlablacarTrips,saveSkyscannerFlights,save_train_bus_trips
from .funtionsRequest.googleMapsRequests import getLatLong_address


def home(request):
    Trip.objects.all().delete()

    if request.method == 'POST':
        form = userRequest(request.POST)
        if form.is_valid():
            gmaps=googlemaps.Client(Request.objects.get('googleMapsRESTApi').APIKey)

            form.cleaned_data['lat_Origin'],form.cleaned_data['lon_Origin']=getLatLong_address(gmaps.geocode(form.cleaned_data['origin_address']))
            form.cleaned_data['lat_Dest'],form.cleaned_data['lon_Dest']=getLatLong_address(gmaps.geocode(form.cleaned_data['destination_address']))
            print('hola')

            # originalDate=form.cleaned_data['date']
            # start_date_local=dt(originalDate.year,originalDate.month,originalDate.day)

            # start_coordinates=str(form.cleaned_data['lat_Origin'])+','+str(form.cleaned_data['lon_Origin'])
            # end_coordinates=str(form.cleaned_data['lat_Dest'])+','+str(form.cleaned_data['lon_Dest'])


            # saveBlablacarTrips(start_coordinates,end_coordinates,start_date_local)
            # saveSkyscannerFlights(start_coordinates,end_coordinates,start_date_local)
            # save_train_bus_trips(start_coordinates,end_coordinates,start_date_local)


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