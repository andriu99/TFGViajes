from app.models import Request,RESTApi,Node
from .usefulFunctions import getProvinceAndLocationThroughCoordinates



def run():
    geoCatalogRequests=Request.objects.get(name='getSkyscannerGeocatalog')
    getTokenRequest=Request.objects.get(name='getTokenSkyscanner')

    #Token
    token=getTokenRequest.executeFunction(getTokenRequest.RApi.BaseUrl,[getTokenRequest.RApi.APIKey])

    #Airports information
    airportsInfo=geoCatalogRequests.executeFunction(geoCatalogRequests.RApi.BaseUrl,[token])

    gMapsGeocodingReverse=Request.objects.get(name='getProLocatDataThroughCoordinates')
    
    for ID,name,lat,lon in airportsInfo:
        location,province=gMapsGeocodingReverse.executeFunction(gMapsGeocodingReverse.RApi.BaseUrl,[lat+','+lon,gMapsGeocodingReverse.RApi.APIKey])
      
        if location=='Unknown':
            location=name
        
        airportNode=Node(code=ID,name=name,latitude=float(lat),longitude=float(lon),nodeType='A',location=location,province=province)
        airportNode.save()