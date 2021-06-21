from ..models import Request,Trip,blablaTrip,skyscannerTrip,busOrTrainTrip
from datetime import timedelta
from ..otherFunctions.dateFunctions import parseDate_withTimeZone,calculateDuration
from ..otherFunctions.nodesFunctions import filterNodes
from django.utils.dateparse import parse_datetime
from ..funtionsRequest.googleMapsRequests import get_locat_province



def saveBlablacarTrips(start_coordinates,end_coordinates,start_date_local):
    set_trips_blabla=set()
    getBlablaCarTrips=Request.objects.get(name='getBlablaCarTrips')

    end_date_local_string=(start_date_local+timedelta(days=1)).isoformat()
    iterableBlablaCar=getBlablaCarTrips.executeFunction([getBlablaCarTrips.RApi.APIKey,start_coordinates,end_coordinates,'EUR',start_date_local.isoformat(),end_date_local_string])
    for (   url,
            startData_str,startData_city,startData_address,startData_latitude,startData_longitude,
            endData_str,endData_city,endData_address,endData_latitude,endData_longitude,
            price

    ) in iterableBlablaCar:


        departureDate_date=parse_datetime(startData_str)
        arrivalDate_date=parse_datetime(endData_str)


        startData_date_withTimeZone = parseDate_withTimeZone(departureDate_date,startData_latitude,startData_longitude) 
        endData_date_withTimeZone = parseDate_withTimeZone(arrivalDate_date,endData_latitude,endData_longitude)


        duration=calculateDuration(startData_date_withTimeZone,endData_date_withTimeZone)
        

        
        new_trip=Trip(departureNode=None,arrivalNode=None,departureDate=departureDate_date,arrivalDate=arrivalDate_date,duration=duration.seconds,price=float(price))
        new_trip.save()
        set_trips_blabla.add(new_trip.pk)



        new_blablatrip=blablaTrip(link=url,
                                    departureCity=startData_city,departureAddress=startData_address,departureLatitude=float(startData_latitude),departureLongitude=float(startData_longitude),
                                    arrivalCity=endData_city,arrivalAddress=endData_address,arrivalLatitude=float(endData_latitude),arrivalLongitude=float(endData_longitude),
                                    trip=new_trip

        )
        new_blablatrip.save()

        return Trip.objects.filter(id__in=set_trips_blabla)


def saveSkyscannerFlights(start_coordinates,end_coordinates,start_date_local):
    set_trips_skys=set()
    getskyscannerTrips=Request.objects.get(name='getTokenSkyscanner')
    token=getskyscannerTrips.executeFunction([getskyscannerTrips.RApi.APIKey])

    getSessionKeySkyscanner=Request.objects.get(name='getSessionKeySkyscanner')
    getFlightsInformationSkyscanner=Request.objects.get(name='getFlightsInformationSkyscanner')
    
    outboundDate='{y}-{m}-{d}'.format(y=str(start_date_local.year),m=str(start_date_local.month).zfill(2),d=str(start_date_local.day).zfill(2))
    
    filter_DepartureNodes=filterNodes(start_coordinates)[0:2]
    filter_ArrivalNodes=filterNodes(end_coordinates)[0:2]
    print(filter_DepartureNodes)
    print(filter_ArrivalNodes)
    for departureNode in filter_DepartureNodes:
        for arrivalNode in filter_ArrivalNodes:
            paramsList=['Economy','ES','EUR','es-ES','iata',departureNode.code,arrivalNode.code,outboundDate,1,0,0,token]
            SessionKey=getSessionKeySkyscanner.executeFunction(paramsList)
            
            getFlightsInformationSkyscanner.PartToaddToBaseUrl+=SessionKey
            results=getFlightsInformationSkyscanner.executeFunction([0,token])

            if results is not None:


                urlList=(getFlightsInformationSkyscanner.PartToaddToBaseUrl.split('/'))
                urlList.pop()
                getFlightsInformationSkyscanner.PartToaddToBaseUrl="/".join(urlList)


                for price,urlPay,departure_date_str,arrival_date_str,duration,airlineName,airlineUrlImage in results:
                    startData_date = parse_datetime(departure_date_str)
                    endData_date = parse_datetime(arrival_date_str)
                    

                    new_trip=Trip(departureNode=departureNode,arrivalNode=arrivalNode,departureDate=startData_date,arrivalDate=endData_date,duration=duration*60,price=float(price))
                    new_trip.save()
                    set_trips_skys.add(new_trip.pk)
                    new_skyscannerTrip=skyscannerTrip(urlPay=urlPay,airlineName=airlineName,airlineUrlImage=airlineUrlImage,trip=new_trip)
                    new_skyscannerTrip.save()

    return Trip.objects.filter(id__in=set_trips_skys)


'''
Guardo los viajes en la BD, y además los incluyo en un array para saber cuáles han sido los últimos guardados.
'''
def save_tripsInfo_DepArriNodes(filter_departureNodes,filter_arrivalNodes,start_date_local,getBusTrainTrips,set_bustrain_Trips=None):
    
    for departure_Node in filter_departureNodes:
        for arrival_Node in filter_arrivalNodes:

            '''
            Solamente buscamos nuevos viajes si no tenemos ningún viaje entre esas dos estaciones en esa fecha.
            Encontramos los viajes entre departure_Node y arrival_NOde en la fecha marcada por el usuario, si no hay buscamos en la api rest.
            '''
            trips=Trip.objects.all().filter(departureDate__year=start_date_local.year,departureDate__month=start_date_local.month,departureDate__day=start_date_local.day).filter(departureNode__code=departure_Node.code).filter(arrivalNode__code=arrival_Node.code)

            if trips.count()==0:
                save_busTrainTrip(departure_Node,arrival_Node,start_date_local,getBusTrainTrips,set_bustrain_Trips)

                        
def save_busTrainTrip(departureNode,arrivalNode,start_date_local,getBusTrainTrips,set_bustrain_Trips=None):
    searchDict=get_SearchDict()

    searchDict['departure_station_id']=int(departureNode.code)
    searchDict['arrival_station_id']=int(arrivalNode.code)
    searchDict['departure_date']=start_date_local.isoformat()

    system_transport_dict=get_systemOfTransport_dict()
    for system in system_transport_dict:
        searchDict['systems']=system_transport_dict[system]
        tripGenerator=getBusTrainTrips.executeFunction(['EUR',searchDict],typeOfData='str')
        
        if tripGenerator!=None:
            for price,departureDate_str,arrivalDate_str in tripGenerator:

                departureDate_date=parse_datetime(departureDate_str)

                if (departureDate_date.replace(tzinfo=None)<(start_date_local+timedelta(days=1))):
                    arrivalDate_date=parse_datetime(arrivalDate_str)

                    departureDate_withTimeZone = parseDate_withTimeZone(departureDate_date,departureNode.latitude,departureNode.longitude)
                
                    arrivalDate_withTimeZone = parseDate_withTimeZone(arrivalDate_date,arrivalNode.latitude,arrivalNode.longitude)
                
                    duration=calculateDuration(departureDate_withTimeZone,arrivalDate_withTimeZone)

                    new_trip=Trip(departureNode=departureNode,arrivalNode=arrivalNode,departureDate=departureDate_date.replace(tzinfo=None),arrivalDate=arrivalDate_date.replace(tzinfo=None),duration=duration.seconds,price=price)
                    new_trip.save()
                    
                    bus_train_trip=busOrTrainTrip(system=system,trip=new_trip)
                    bus_train_trip.save()
                    if set_bustrain_Trips!=None:
                        set_bustrain_Trips.add(new_trip.pk)





def get_SearchDict():

    searchDict={
            "passenger_ids": [
            "314892886"
            ],
            "card_ids": [
            "14127110"
            ],
            "departure_station_id":0,
            "arrival_station_id":0,
            "departure_date":"2021-03-29T00:00:00+01:00",
            "systems":[]
        }

    return searchDict

def get_systemOfTransport_dict():

    return {
        'T':['renfe'],
        'B':['busbud']
    }




def save_train_bus_trips(filter_departureNodes,filter_arrivalNodes,locatO,locatD,start_date_local):

    # locatO,provO=get_locat_province(start_coordinates)
    # locatD,provD=get_locat_province(end_coordinates)
     

    # filter_departureNodes=filterNodes(start_coordinates,nodeType='S',location=locatO,province=provO)
    # filter_arrivalNodes=filterNodes(end_coordinates,nodeType='S',location=locatD,province=provD)
    
    '''
    Buscamos en la caché de la BD:
        -Viajes que comiencen en el día marcado por el usuario y que su nodo de partida tenga la localización igual a la 
        de partida del viaje, e igual para el de llegada.

    '''
    set_bustrain_Trips=set()
    for bus_trainTrip in busOrTrainTrip.objects.all():
        actual_trip=bus_trainTrip.trip

        if (actual_trip.departureDate>=start_date_local and actual_trip.departureDate<=(start_date_local+timedelta(days=1))):
            if(actual_trip.departureNode.location==locatO and actual_trip.arrivalNode.location==locatD):
                set_bustrain_Trips.add(actual_trip.pk)
        
    if not set_bustrain_Trips: 
        getBusTrainTrips=Request.objects.get(name='getbustrainTripsInformationTrainline')
        
      
        save_tripsInfo_DepArriNodes(filter_departureNodes,filter_arrivalNodes,start_date_local,getBusTrainTrips,set_bustrain_Trips)
    
    query_set_bustrain_Trips=Trip.objects.filter(id__in=set_bustrain_Trips)
    return query_set_bustrain_Trips


'''
Con los arcos obtengo un diccionario cuya clave es el nodo de origen 
Y cuyo valor es un diccionario cuyas claves serán los nodos (destino) que tienen viajes con el nodo de origen.
El valor de este último diccionario será un diccionario con claves igual al id de cada viaje entre nodo origen y destino.
Para cada viaje se almacena una lista con [precio, fecha de partida, fecha de llegada]

'''

def Convert_listOfList_intoDict(tups):
    dct_ids_price_dates=dict()
    for x,y,trip_id,trip_price in tups:
        
        if x not in dct_ids_price_dates.keys():
            dct_ids_price_dates[x]={}

        if y not in dct_ids_price_dates[x].keys():
            dct_ids_price_dates[x][y]=dict()

        dct_ids_price_dates[x][y][trip_id]=list()
        dct_ids_price_dates[x][y][trip_id].append(trip_price)
        dct_ids_price_dates[x][y][trip_id].append(Trip.objects.get(pk=trip_id).departureDate)
        dct_ids_price_dates[x][y][trip_id].append(Trip.objects.get(pk=trip_id).arrivalDate)


    return dct_ids_price_dates



def init_dijkstra(path,adj_node,queue,node):
        path[node] = float("inf")

        '''
        El primer elemento de la lista será el nodo desde el cuál se llega
        El segundo será el viaje concreto desde el cuál se llega.
        '''
        adj_node[node] = [None,None]
        if node not in queue:
            queue.append(node)



'''
Recorremos los nodos desde el nodo destino al inicial.
Vamos almacenando los viajes recursivamente.

'''
def get_list_trips(solution_dijkstra,code_arrivalNode):

    list_trips_ids=list()
    x=code_arrivalNode
    while True:
        if solution_dijkstra[x][1] is None:
            break 

        list_trips_ids.append(Trip.objects.get(pk=solution_dijkstra[x][1]))

        x = solution_dijkstra[x][0]
       
        
        


    return list_trips_ids[:: -1]


'''
graph: Diccionario obtenido en Convert_listOfList_intoDict
initial: código del nodo que queremos considerar como inicial.


'''
def dijkstra(graph,initial):   

    path = dict() #Nos indica el coste total hasta llegar a cada nodo


    '''
    Diccionario que tedrá como key un nodo y como value una lista [1,2].
    Donde 1 será el nodo a través del cuál llegamos a el y 2 el viaje en concreto (id),
    por el que llegamos.

    '''
    adj_node = dict() 

    #Nodos del grafo todavía no chequeados
    queue = list()



    '''
    Iniciamos cada nodo en el grafo.
    '''
    for node in graph.keys():
        init_dijkstra(path,adj_node,queue,node)



    for dict_arrivalNode_trips in graph.values():
        for arrivalNode in dict_arrivalNode_trips:
            init_dijkstra(path,adj_node,queue,arrivalNode)
    
     

    path[initial] = 0

   
    while queue:
        # find min distance which wasn't marked as current
        key_min = queue[0]
        min_val = path[key_min]
        for n in range(1, len(queue)):
            if path[queue[n]] < min_val:
                key_min = queue[n]  
                min_val = path[key_min]

        cur = key_min
        queue.remove(cur)

        if cur in graph.keys():
            for i in graph[cur]:
                #Elijo de todos los viaje entre el nodo actual y el nodo i el más conveniente

                #Primero ordeno los viajes según la clave (precio/duration)
                sorted_trips={k: v for k, v in sorted(graph[cur][i].items(), key=lambda item: item[1])}
                for trip_id in sorted_trips:
                    trip_price_or_duration=sorted_trips[trip_id][0]

                    alternate=trip_price_or_duration+path[cur]
                     



                    if alternate<path[i]: #Si la alternativa es mejor a la actual en cuanto a precio/duración


                        '''
                        Comprobamos si es además factible teniendo en cuenta
                        horarios.

                        Recorremos los nodos desde el destino al origen recursivamente.

                        Previous en un principio es el nodo destino y actual node el nodo anterior al destino.
                        Recursivamente previous pasa a ser el actual, y así sucesivamente.
                        '''
                        trip_date_start_previous=sorted_trips[trip_id][1]
                        
                        actual_node=cur
                        previous=i

                        is_solution=True
                        while True:
                            previous = actual_node
                            actual_node=adj_node[actual_node][0]

                            if actual_node is None: 
                                break
                            
                            actual_trip_id=adj_node[previous][1] #Id del viaje que une actual_node con previous

                            if actual_trip_id is not None:
                                departureTime_actualTrip=graph[actual_node][previous][actual_trip_id][0]
                                arrivalTime_actualTrip=graph[actual_node][previous][actual_trip_id][1]
                            else:
                                arrivalTime_actualTrip=None


                            ''' 
                            Si en tiempo de llegada es mayor que el tiempo de comienzo del viaje siguiente, esta combinación
                            no es válida

                            '''
                            if arrivalTime_actualTrip is not None and arrivalTime_actualTrip<trip_date_start_previous:
                                trip_date_start_previous=departureTime_actualTrip

                            else:
                                is_solution=False
                                break

                        if is_solution:
                            
                            path[i] = alternate
                            adj_node[i] = [cur,trip_id]
                            break
                            
        
        elif initial==cur:
            break
        
 
    return adj_node

'''
Búsqueda de viajes con transbordos.

'''


def more_Trips(start_date,filter_departureNodes,filter_arrivalNodes):
    list_oflist_travelswithTransfer_id=list() #Lista que guarda listas con los viajes encadenados que son solución

    # filter_departureNodes=filterNodes(start_coordinates,nodeType='S')
    # filter_arrivalNodes=filterNodes(end_coordinates,nodeType='S')
   
    '''
    Lista de los viajes guardados en la BD que cumplen:
        - Su fecha de inicio está dentro del día que el usuario ha marcado.

    '''
    trips=Trip.objects.all().filter(departureDate__year=start_date.year,departureDate__month=start_date.month,departureDate__day=start_date.day)


    '''
    Relleno la lista de arcos del grafo.
    Cada arco tiene la siguiente estructura, es una lista con:
        1)Código del nodo de partida
        2)Código del nodo de destino
        3)Id del viaje
        4)Precio del viaje 
    '''
    list_edges=list()

    for trip in trips:

        if (hasattr(trip,"busOrTrainTrip")):
            list_edge=list()

            list_edge.append(trip.departureNode.code)
            list_edge.append(trip.arrivalNode.code)

            list_edge.append(trip.id)

            list_edge.append(trip.price)
            list_edges.append(list_edge)

     

    
    
    dct_ids_price_dates=Convert_listOfList_intoDict(list_edges)

    
    '''
    Por cada posible nodo origen:
        -Ejecutamos dijkstra para encontramos los caminos óptimos.
        -Conseguimos para cada posible nodo destino una lista de viajes para llegar a el (si es posible).

    '''
    for departureNode in filter_departureNodes:

        sol_dijkstra=dijkstra(dct_ids_price_dates,departureNode.code)


        for arrivalNode in filter_arrivalNodes:
            sol_trips=get_list_trips(sol_dijkstra,arrivalNode.code)


            firstTrip_node=sol_trips[0].departureNode.code
            if firstTrip_node==departureNode.code:
                list_oflist_travelswithTransfer_id.append(sol_trips)
            


    return list_oflist_travelswithTransfer_id
