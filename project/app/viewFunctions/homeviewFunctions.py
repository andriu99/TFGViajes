from networkx.algorithms.shortest_paths import weighted
from ..models import Request,Trip,blablaTrip,skyscannerTrip,busOrTrainTrip,Node
from datetime import timedelta
from ..otherFunctions.dateFunctions import parseDate_withTimeZone,calculateDuration
from ..otherFunctions.nodesFunctions import filterNodes
from django.utils.dateparse import parse_datetime
from ..funtionsRequest.googleMapsRequests import get_locat_province
import networkx as nx
import matplotlib.pyplot as plt    
from datetime import datetime as dt
import random


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
    
    filter_DepartureNodes=filterNodes(start_coordinates)
    filter_ArrivalNodes=filterNodes(end_coordinates)
    for departureNode in filter_DepartureNodes:
        for arrivalNode in filter_ArrivalNodes:
            paramsList=['Economy','ES','EUR','es-ES','iata',departureNode.code,arrivalNode.code,outboundDate,1,0,0,token]
            SessionKey=getSessionKeySkyscanner.executeFunction(paramsList)
            getFlightsInformationSkyscanner.PartToaddToBaseUrl+=SessionKey
            results=getFlightsInformationSkyscanner.executeFunction([0,token])


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
    
    for departureNode in filter_departureNodes:
        for arrivalNode in filter_arrivalNodes:
            save_busTrainTrip(departureNode,arrivalNode,start_date_local,getBusTrainTrips,set_bustrain_Trips)

                        
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




def save_train_bus_trips(start_coordinates,end_coordinates,start_date_local):

    locatO,provO=get_locat_province(start_coordinates)
    locatD,provD=get_locat_province(end_coordinates)

    filter_departureNodes=filterNodes(start_coordinates,nodeType='S')
    filter_arrivalNodes=filterNodes(end_coordinates,nodeType='S')
    

    #Buscamos en la caché de la BD:
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



# def dijkstra(graph,dict_times):   

#     initial = 'B'
#     dict_arrivalTime_node={}

#     path = {}

#     adj_node = {}

#     queue = []


#     for node in graph:
#         path[node] = float("inf")
#         adj_node[node] = None
#         dict_arrivalTime_node[node]=None
#         queue.append(node)
        
#     path[initial] = 0

#     while queue:
#         # find min distance which wasn't marked as current
#         # print(adj_node)
#         key_min = queue[0]
#         min_val = path[key_min]
#         for n in range(1, len(queue)):
#             if path[queue[n]] < min_val:
#                 # current_time=dict_times[]
#                 key_min = queue[n]  
#                 min_val = path[key_min]
#         cur = key_min

#         queue.remove(cur)
        

#         for i in graph[cur]:
#             trip_data_end=dict_times[cur][i]
#             alternate = graph[cur][i] + path[cur]
#             # print(dict_arrivalTime_node[i])
#             # print(trip_data_end)
#             if path[i] > alternate: #and (dict_arrivalTime_node[i] is None or trip_data_end>dict_arrivalTime_node[i]):
                
#                 actual_node=cur
#                 previus=i

#                 is_better=True

#                 last_time=dict_times[cur][previus]
#                 print('Tiempo inicial')
#                 print(last_time)
#                 while True:


#                     print(cur,previus)
#                     previus = actual_node
#                     actual_node=adj_node[actual_node]
#                     # print(previus,actual_node)


#                     if actual_node is None:
#                         print("")
#                         break

#                     time_actual=dict_times[actual_node][previus]
#                     print(time_actual,actual_node,previus)
#                     if last_time>time_actual:
#                         last_time=time_actual
#                     else:
#                         print('Es peor')
#                         print(last_time)
#                         print(time_actual)
#                         is_better=False
#                         break
                    

#                 print('Fin bucle')
              

#                 if is_better:
#                     path[i] = alternate
#                     adj_node[i] = cur
#                     dict_arrivalTime_node[i]=trip_data_end
                    

#                 # print(graph[cur][i])
                    

#             # else:
#             #     print('Eooo')
                
                
#     x = 'F'
#     # print('The path between B to F')
#     # print(x, end = '<-')
#     print(adj_node)
    
#     print('The path between A to F')
#     print(x, end = '<-')
#     while True:
#         x = adj_node[x]
#         if x is None:
#             print("")
#             break
#         print(x, end='<-')



#     for key in (dict_times):
#         print(key)
#         print(dict_times[key])



# def Convert_listOfList_intoDict(tups):
#     dct_weights=dict()
#     dct_times=dict()
#     # num=0
#     for x,y,element in tups:
#         if x not in dct_weights.keys():
#             dct_weights[x]={}
#             dct_times[x]={}

#         dct_weights[x][y]=element['weight']
#         # if random.randint(0,100)>50:
#         #     dct_times[x][y]=dt(2021,6,15,num)
#         #     num+=1
#         # else:
#         dct_times[x][y]=dt(2021,6,15,random.randint(0,23))


#     return dct_weights,dct_times


# def get_dict_DateTime(dict_edges):
#     for key in dict_edges.keys():
#         for element in key:
#             print(element)


            
# def more_Trips():
    
#     DG=nx.DiGraph()
#     DG.add_nodes_from(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
#     list_weight=[['B', 'A', 5], ['B', 'D', 1], ['B', 'G', 2], ['A', 'B', 5], ['A', 'D', 3], ['A', 'E', 12], ['A', 'F', 5], ['D', 'B', 1], ['D', 'G', 1], ['D', 'E', 1], ['D', 'A', 3], ['G', 'B', 2], ['G', 'D', 1], ['G', 'C', 2], ['C', 'G', 2], ['C', 'E', 1], ['C', 'F', 16], ['E', 'A', 12], ['E', 'D', 1], ['E', 'C', 1], ['E', 'F', 2], ['F', 'A', 5], ['F', 'E', 2], ['F', 'C', 16]]
#     # list_time = [i[:] for i in list_weight]

#     # for i in list_time:
#     #     i[-1]=dt(2021,6,15,random.randint(0, 23))




#     DG.add_weighted_edges_from(list_weight)
#     # labels = nx.get_edge_attributes(DG,'weight')
#     # pos = nx.spring_layout(DG)

#     # nx.draw_networkx(DG,
#     #              node_color="lightblue",
#     #              edge_color="gray",
#     #              font_size=24,
#     #              width=2, with_labels=True, node_size=3500,
#     #              pos=pos,
#     # )


    
#     # nx.draw_networkx_edge_labels(DG,pos, edge_labels=labels)


#     # plt.show()

  

#     dict_edges,dict_times=Convert_listOfList_intoDict(DG.edges(data=True))

#     # get_dict_DateTime(dict_edges)


#     # print(dict_edges)
#     # print(id(list_time))
#     # print(id(list_weight))
#     # print(list_time==list_weight)
#     # for i in range(0,20):
#     (dijkstra(dict_edges,dict_times))





def Convert_listOfList_intoDict(tups):
    dct_ids_price_dates=dict()
    # dct_times=dict()
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
        queue.append(node)




def dijkstra(graph):   



    print(graph)


    initial = '23776'

    path = {}

    adj_node = {}

    #Número de viajes chequeados que tengan como inicio el nodo marcado como key
    queue = []

    for node in graph.keys():
        init_dijkstra(path,adj_node,queue,node)



    for dict_arrivalNode_trips in graph.values():
        for arrivalNode in dict_arrivalNode_trips:
            init_dijkstra(path,adj_node,queue,arrivalNode)
    
    print(path)
    print(adj_node)
    print(queue)
    
     

    path[initial] = 0
     
    
    while queue:
        # find min distance which wasn't marked as current
        key_min = queue[0]
        min_val = path[key_min]
        for n in range(1, len(queue)):
            if path[queue[n]] < min_val:
                # current_time=dict_times[]
                key_min = queue[n]  
                min_val = path[key_min]
        cur = key_min

        queue.remove(cur)

        


        

        for i in graph[cur]:

            #Elijo de todos los viaje entre el nodo actual y el nodo i el más conveniente

            #Primero ordeno los viajes según la clave (precio/duration)
            sorted_trips={k: v for k, v in sorted(graph[cur][i].items(), key=lambda item: item[1])}
            for trip_id in sorted_trips:

                trip_price_or_duration=sorted_trips[trip_id][0]
                alternate=trip_price_or_duration+path[cur]

                if alternate<path[i]: #Si la alternativa es mejor a la actual

                    '''
                    Comprobamos si es además factible teniendo en cuenta
                    horarios.

                    Recorremos los nodos desde el destino al origen recursivamente.
                    '''
                    trip_date_start_previous=sorted_trips[trip_id][0]
                    
                    actual_node=cur
                    previous=i

                    is_solution=True
                    while True:
                        previous = actual_node
                        actual_node=adj_node[actual_node][0]

                        if actual_node is None:
                            break
                        
                        
                        departureTime_actualTrip=graph[actual_node][previous][trip_id][0]
                        arrivalTime_actualTrip=graph[actual_node][previous][trip_id][1]


                        if arrivalTime_actualTrip<trip_date_start_previous:
                            trip_date_start_previous=departureTime_actualTrip

                        else:
                            is_solution=False
                            break

                    if is_solution:
                        path[i] = alternate
                        adj_node[i] = [cur,trip_id]
                        break

        
    x = 'F'
    print('The path between A to F')
    print(x, end = '<-')

    list_trips_ids=list()
    while True:
        x = adj_node[x][0]
        list_trips_ids.append(adj_node[x][1])
        if x is None:
            print("")
            break
        print(x, end='<-')

    return [ele for ele in reversed(list_trips_ids)]

            

                    

'''
            trip_data_end=dict_times[cur][i]
            alternate = graph[cur][i] + path[cur]
            # print(dict_arrivalTime_node[i])
            # print(trip_data_end)
            if path[i] > alternate: #and (dict_arrivalTime_node[i] is None or trip_data_end>dict_arrivalTime_node[i]):
                
                actual_node=cur
                previus=i

                is_better=True

                last_time=dict_times[cur][previus]
                print('Tiempo inicial')
                print(last_time)
                while True:


                    print(cur,previus)
                    previus = actual_node
                    actual_node=adj_node[actual_node]
                    # print(previus,actual_node)


                    if actual_node is None:
                        print("")
                        break

                    time_actual=dict_times[actual_node][previus]
                    print(time_actual,actual_node,previus)
                    if last_time>time_actual:
                        last_time=time_actual
                    else:
                        print('Es peor')
                        print(last_time)
                        print(time_actual)
                        is_better=False
                        break
                    

                print('Fin bucle')
              

                if is_better:
                    path[i] = alternate
                    adj_node[i] = cur
                    dict_arrivalTime_node[i]=trip_data_end
                    

                
                
                
    x = 'F'
    # print('The path between B to F')
    # print(x, end = '<-')
    print(adj_node)
    
    print('The path between A to F')
    print(x, end = '<-')
    while True:
        x = adj_node[x]
        if x is None:
            print("")
            break
        print(x, end='<-')
'''

def more_Trips(start_date):
    



    trips=Trip.objects.all().filter(departureDate__year=start_date.year,departureDate__month=start_date.month,departureDate__day=start_date.day)

    list_edges=list()

    for trip in trips:

        set_nodes=set()
        if (hasattr(trip,"busOrTrainTrip")):
            list_edge=list()


            set_nodes.add(trip.arrivalNode.code)
            set_nodes.add(trip.departureNode.code)

            list_edge.append(trip.arrivalNode.code)
            list_edge.append(trip.departureNode.code)
            list_edge.append(trip.id)

            list_edge.append(trip.price)
            list_edges.append(list_edge)

     

   
    
    dct_ids_price_dates=Convert_listOfList_intoDict(list_edges)
    print(dct_ids_price_dates['22676']['6615'][16123])
    # print(dct_ids_price_dates)

    # for trip_info in (dct_ids_price_dates['22676']['6615']):
    #     print(dct_ids_price_dates['22676']['6615'][trip_info][2])

    
    # for i in (dct_ids_price_dates['22676']):
    #     print('COn '+i)
    #     aux={k: v for k, v in sorted(dct_ids_price_dates['22676'][i].items(), key=lambda item: item[1])}
    #     for trip_id in aux:
    #         print(aux[trip_id][0])
    #         print(aux[trip_id][1])
    #         print(aux[trip_id][2])




    # print(len(dct_ids_price_dates['22676']))

    # dijkstra(dct_ids_price_dates)


   
    
