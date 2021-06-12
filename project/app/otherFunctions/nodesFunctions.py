from django.db.models.expressions import F
from ..models import Node
from ..funtionsRequest.googleMapsRequests import getTime_between_coordinates,get_locat_province

def filterNodes(coordinates,nodeType='A'):
    location,province=get_locat_province(coordinates)

    filter_Nodes=Node.objects.filter(location=location,nodeType=nodeType)
    if not filter_Nodes.exists() or location=="Unknown":
        filter_Nodes=Node.objects.filter(province=province,nodeType=nodeType)


        if nodeType!='A':
            filter_Nodes = filter_Nodes.annotate(time_to_go=0*F('latitude')) #Añado el campo distancia a las coordenadas a cada nodo


            for node in filter_Nodes:
                lat=node.latitude
                lng=node.longitude
                time=getTime_between_coordinates(coordinates,str(lat)+','+str(lng))        
                node.time_to_go=time    
            
            filter_Nodes=filter_Nodes.order_by('time_to_go')
            return filter_Nodes[0:10]


    return filter_Nodes

