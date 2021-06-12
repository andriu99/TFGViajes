from django.db.models.expressions import F
from ..models import Request,Node,RESTApi
import googlemaps as gmaps
from ..funtionsRequest.googleMapsRequests import getTime_between_coordinates

def filterNodes(coordinates,nodeType='A'):
    getProLocatDataThroughCoordinates=Request.objects.get(name='getProLocatDataThroughCoordinates')
    location,province=getProLocatDataThroughCoordinates.executeFunction([coordinates,getProLocatDataThroughCoordinates.RApi.APIKey])

    filter_Nodes=Node.objects.filter(location=location,nodeType=nodeType)
    if not filter_Nodes.exists() or location=="Unknown":
        filter_Nodes=Node.objects.filter(province=province,nodeType=nodeType)


        if nodeType!='A':
            filter_Nodes = filter_Nodes.annotate(time_to_go=0*F('latitude')) #Añado el campo distancia a las coordenadas a cada nodo

            ClientGMaps=gmaps.Client(RESTApi.objects.get(name='googleMapsRESTApi').APIKey)

            for node in filter_Nodes:
                lat=node.latitude
                lng=node.longitude
                resultJson=ClientGMaps.distance_matrix(origins=coordinates,destinations=str(lat)+','+str(lng))
                time=getTime_between_coordinates(resultJson)        
                node.time_to_go=time    
            
            filter_Nodes=filter_Nodes.order_by('time_to_go')
            return filter_Nodes[0:10]


    return filter_Nodes

