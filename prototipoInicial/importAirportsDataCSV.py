import csv
import requests
from clasesAPIRest import RESTApi,getRequests
from planesFunctions import getToken,getAirportsData

params={
    'apiKey':''
}

#Token Requests:
getTokenFromSkyscanner=getRequests('get token from skyscanner','token/v2/gettoken',params,getToken)
getAirportsData=getRequests('get minformation about the airport from skysanner', 'geo/v1.0', params, getAirportsData)

#Skyscanner rest api:
SkyscannerRESTAPI=RESTApi('https://partners.api.skyscanner.net/apiservices/', 'prtl6749387986743898559646983194')

#Add requests to skyscanner rest api
SkyscannerRESTAPI.addRequests(getTokenFromSkyscanner)
SkyscannerRESTAPI.addRequests(getAirportsData)

#Get a token:
responseToken=SkyscannerRESTAPI.getRequests()[0].execute(SkyscannerRESTAPI.getBaseUrl(),[SkyscannerRESTAPI.getAPIKey()])
token=SkyscannerRESTAPI.getRequests()[0].extractDataFromJson(responseToken.json())

#Get airports data:
responseAirports=SkyscannerRESTAPI.getRequests()[1].execute(SkyscannerRESTAPI.getBaseUrl(),[token])
airportsIterableData=SkyscannerRESTAPI.getRequests()[1].extractDataFromJson(responseAirports.json())


#Abrimos el fichero de escritura:
with open("airportsSpain.txt", 'w', newline = '',encoding='utf-8') as outfile:
    csv_writer = csv.writer(outfile, delimiter = ',')
    for airportId,airportName,airportLatitude,airportLongitude in airportsIterableData:
        csv_writer.writerow([airportId,airportName,airportLatitude,airportLongitude])

        



