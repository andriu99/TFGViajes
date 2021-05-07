from app.models import Request,RESTApi,Node
from .usefulFunctions import getProvinceAndLocationThroughCoordinates



def run():
    geoCatalogRequests=Request.objects.get(name='getSkyscannerGeocatalog')
    getTokenRequest=Request.objects.get(name='getTokenSkyscanner')

    #Token
    token=getTokenRequest.executeFunction([getTokenRequest.RApi.APIKey])

    #Airports information
    airportsInfo=geoCatalogRequests.executeFunction([token])
    
    
    for ID,name,lat,lon in airportsInfo:
        location,province=getProvinceAndLocationThroughCoordinates(lat,lon)
      

        if location=='Unknown':
            location=name
        
        airportNode=Node(code=ID,name=name,latitude=float(lat),longitude=float(lon),nodeType='A',location=location,province=province)
        airportNode.save()

