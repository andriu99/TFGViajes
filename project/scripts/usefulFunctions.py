from app.models import Request


def getProvinceAndLocationThroughCoordinates(latitude,longitude):
    geoCatalogRequests=Request.objects.get(name='getProLocatDataThroughCoordinates')
    location,province=geoCatalogRequests.executeFunction(geoCatalogRequests.RApi.BaseUrl,[latitude+','+longitude,geoCatalogRequests.RApi.APIKey])
    return location,province