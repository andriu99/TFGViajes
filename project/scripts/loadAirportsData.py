from app.models import Request,RESTApi,Node

skyscannerRESTApi=RESTApi.objects.get(name='SkyscannerRESTApi') 

geoCatalogRequests=Request.objects.get(name='getSkyscannerGeocatalog')
getTokenRequest=Request.objects.get(name='getTokenSkyscanner')

#Token
token=getTokenRequest.executeFunction(skyscannerRESTApi.BaseUrl,[skyscannerRESTApi.APIKey])

#Airports information
#airportsInfo=geoCatalogRequests.executeFunction(skyscannerRESTApi.APIKey,[token],"dict")
