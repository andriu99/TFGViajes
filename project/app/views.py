
from django.shortcuts import render
from .forms import userRequest
from .models import Trip
from datetime import datetime as dt 
from .viewFunctions.homeviewFunctions import more_Trips, saveBlablacarTrips,saveSkyscannerFlights,save_train_bus_trips
from django.contrib import messages


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

            date=form.cleaned_data['date']
            start_date=dt(date.year,date.month,date.day)
    
            start_coordinates=str(form.cleaned_data['lat_Origin'])+','+str(form.cleaned_data['lon_Origin'])
            end_coordinates=str(form.cleaned_data['lat_Dest'])+','+str(form.cleaned_data['lon_Dest'])


            exists_blablaTrip=True
            exist_skyscannerTrip=True
            exist_busTrainTrip=True

            # try:
            #     blablaTrips=saveBlablacarTrips(start_coordinates,end_coordinates,start_date)
            # except:
            #     exists_blablaTrip=False
            #     messages.error(request,'Error al procesar los viajes en blablacar')

            # try:
            #     skyscannerTrips=saveSkyscannerFlights(start_coordinates,end_coordinates,start_date)
            # except:
            #     exist_skyscannerTrip=False
            #     messages.error(request,'Error al procesar los viajes en skyscanner')

            print('Aca')

            try:
                trips_busTrain=save_train_bus_trips(start_coordinates,end_coordinates,start_date)
            except:
                exist_busTrainTrip=False
                messages.error(request,'Error al procesar los viajes en bus y tren')

                
            # more_Trips(start_date,start_coordinates,end_coordinates)
            exists_blablaTrip=(exists_blablaTrip and blablaTrips!=None)
            exist_skyscannerTrip=(exist_skyscannerTrip and skyscannerTrips!=None)
            exist_busTrainTrip=(exist_busTrainTrip and trips_busTrain!=None)

            #Filtro el precio:
            if form.cleaned_data['maxPrice']!=None:

                if  exists_blablaTrip:
                    blablaTrips=blablaTrips.filter(price__lt=form.cleaned_data['maxPrice'])

                if  exist_skyscannerTrip:
                    skyscannerTrips=skyscannerTrips.filter(price__lt=form.cleaned_data['maxPrice'])

                if  exist_busTrainTrip:
                    trips_busTrain=trips_busTrain.filter(price__lt=form.cleaned_data['maxPrice'])


            

            #Aplico la ordenación (si procede):
            if form.cleaned_data['OrderType']!='NONE':
                order_type=''


                if  form.cleaned_data['OrderType']=='DESC':
                    order_type+='-'

                order_by=str(form.cleaned_data['OrderBy']).lower()  

                if exists_blablaTrip:
                    blablaTrips=blablaTrips.order_by(order_type+order_by) 

                if exist_skyscannerTrip:
                    skyscannerTrips=skyscannerTrips.order_by(order_type+order_by)

                if exist_busTrainTrip:
                    trips_busTrain=trips_busTrain.order_by(order_type+order_by)


    else:
        
        form = userRequest()


   

    try:
        busTrips=trips_busTrain.filter(busOrTrainTrip__system='B')
    except:
        busTrips={}

    try:
        trainTrips=trips_busTrain.filter(busOrTrainTrip__system='T')
    except:
        trainTrips={}


    
    '''
    blablaTrips,skyscannerTrips,busTrips,trainTrips => Pertenecen al modelo Trip
    '''
    context = {'form' : form,'blablaTrips':blablaTrips,'skyscannerTrips':skyscannerTrips,'busTrips':busTrips,'trainTrips':trainTrips}
    return render(request,'app/home.html',context=context)


def new(request):
    return render(request,'app/new.html')