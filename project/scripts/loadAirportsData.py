from app.models import Request,RESTApi,Node


def getProvinceAndLocationThroughCoordinates(latitude,longitude):
    geoCatalogRequests=Request.objects.get(name='getProLocatDataThroughCoordinates')
    location,province=geoCatalogRequests.executeFunction(geoCatalogRequests.RApi.BaseUrl,[latitude+','+longitude,geoCatalogRequests.RApi.APIKey])
    return province,location

def run():
    skyscannerRESTApi=RESTApi.objects.get(name='SkyscannerRESTApi') 

    geoCatalogRequests=Request.objects.get(name='getSkyscannerGeocatalog')
    getTokenRequest=Request.objects.get(name='getTokenSkyscanner')

    #Token
    token=getTokenRequest.executeFunction(skyscannerRESTApi.BaseUrl,[skyscannerRESTApi.APIKey])
    token

    #Airports information
    airportsInfo=geoCatalogRequests.executeFunction(skyscannerRESTApi.BaseUrl,[token])
    
    for ID,name,lat,lon in airportsInfo:
        location,province=getProvinceAndLocationThroughCoordinates(lat,lon)
        
        airportNode=Node(code=ID,name=name,latitude=float(lat),longitude=float(lon),nodeType='A',location=location,province=province)
        airportNode.save()

