import csv
from app.models import Request,RESTApi,Node


blablaCarRESTApi=RESTApi('https://public-api.blablacar.com','UIbM2vkhEdrrTLiLnrQkBqgPxrv7S4mI')
blablaCarRESTApi.save()
findBlablaTrips=Request('Find Trips with dates and coordinates','/api/v3/trips','findBlablaTrips','GET',RApi=blablaCarRESTApi)




skyscannerRESTApi=RESTApi('https://partners.api.skyscanner.net/apiservices/','prtl6749387986743898559646983194')

skyscannerRESTApi.save()



trainlineRESTApi=RESTApi('https://www.trainline.eu/api/v5_1/','A8fQLJDF94cPUKEu3Vpi')
trainlineRESTApi.save()