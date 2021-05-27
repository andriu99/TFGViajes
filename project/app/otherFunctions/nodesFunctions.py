from app.models import Request,Node


def filterNodes(coordinates,nodeType='A'):
    getProLocatDataThroughCoordinates=Request.objects.get(name='getProLocatDataThroughCoordinates')
    location,province=getProLocatDataThroughCoordinates.executeFunction([coordinates,getProLocatDataThroughCoordinates.RApi.APIKey])

    filter_Nodes=Node.objects.filter(location=location,nodeType=nodeType)
    if not filter_Nodes.exists() or location=="Unknown":
        filter_Nodes=Node.objects.filter(province=province,nodeType=nodeType)

    return filter_Nodes

