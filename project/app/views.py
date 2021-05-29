
from django.shortcuts import render
from .forms import userRequest
from app.models import blablaTrip,skyscannerTrip,Trip,Node,RESTApi,busOrTrainTrip
from datetime import datetime as dt 
from .viewFunctions.homeviewFunctions import saveBlablacarTrips,saveSkyscannerFlights,save_train_bus_trips
import googlemaps as gmaps
from .funtionsRequest.googleMapsRequests import getProvinceLocationThroughCoordinates

def home(request):

    blablaTrips={}
    skyscannerTrips={}
    trips_busTrain={}


    if request.method == 'POST':
        form = userRequest(request.POST)
        if form.is_valid():

            id_delete=set()
            for trip in Trip.objects.all():
                if (hasattr(trip,"busOrTrainTrip")==False):
                    id_delete.add(trip.id)

            Trip.objects.all().filter(id__in=id_delete).delete() #Borro los viajes en avión y en blablacar

            print(form.cleaned_data['OrderType'])
            date=form.cleaned_data['date']
            start_date_local=dt(date.year,date.month,date.day)
    
            start_coordinates=str(form.cleaned_data['lat_Origin'])+','+str(form.cleaned_data['lon_Origin'])
            end_coordinates=str(form.cleaned_data['lat_Dest'])+','+str(form.cleaned_data['lon_Dest'])

            blablaTrips=saveBlablacarTrips(start_coordinates,end_coordinates,start_date_local)
            skyscannerTrips=saveSkyscannerFlights(start_coordinates,end_coordinates,start_date_local)
            trips_busTrain=save_train_bus_trips(start_coordinates,end_coordinates,start_date_local)

            #Filtro el precio:
            if form.cleaned_data['maxPrice']!=None:
                blablaTrips=blablaTrips.filter(price__lt=form.cleaned_data['maxPrice'])
                skyscannerTrips=skyscannerTrips.filter(price__lt=form.cleaned_data['maxPrice'])
                trips_busTrain=trips_busTrain.filter(price__lt=form.cleaned_data['maxPrice'])


            set_bus_trainTrips=set()
            set_bus_trainTrips_trips=set()


            for bus_trainTrip in trips_busTrain:
                set_bus_trainTrips.add(bus_trainTrip.busOrTrainTrip.pk)
                set_bus_trainTrips_trips.add(bus_trainTrip.busOrTrainTrip.pk)


            bus_trainTrips=busOrTrainTrip.objects.filter(id__in=set_bus_trainTrips)
            bus_trainTrips_trips=Trip.objects.filter(id__in=set_bus_trainTrips_trips)

            #Aplico la ordenación (si procede):
            # if form.cleaned_data['OrderType']!='NONE':
            #     order_type=''
            #     if form.cleaned_data['OrderType']=='ASC':
            #         order_type+='+'

            #     if  form.cleaned_data['OrderType']=='DESC':
            #         order_type+='-'

            #     order_by=str(form.cleaned_data['OrderBy']).lower()  

            #     blablaTrips.order_by(order_type+order_by)
            #     skyscannerTrips.order_by(order_type+order_by)
            #     trips_busTrain.order_by(order_type+order_by)


    else:

        form = userRequest()

   

    try:
        busTrips=bus_trainTrips.filter(system='B')
    except:
        busTrips={}

    try:
        trainTrips=bus_trainTrips.filter(system='T')
    except:
        trainTrips={}

    
    '''
    blablaTrips,skyscannerTrips => Pertenecen a los modelos blablaTrip y skyscannerTrip
    busTrips,trainTrips => Pertenecen al modelo Trip
    '''
    context = {'form' : form,'blablaTrips':blablaTrips,'skyscannerTrips':skyscannerTrips,'busTrips':busTrips,'trainTrips':trainTrips}
    return render(request,'app/home.html',context=context)


def new(request):
    return render(request,'app/new.html')