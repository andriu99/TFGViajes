import requests
import urllib.parse
import numpy as np
import json
from datetime import datetime as dt
# response = requests.request("GET", 'https://partners.api.skyscanner.net/apiservices/token/v2/gettoken?apiKey={apiKey}'.format(apiKey='ra66933236979928'))


# token=response.text
# print(urllib.parse.quote(token))
"""
Encuentra el código del aeropuerto de la ciudad deseada vía API-REST
"""
def FindAirport(StrPlaceName):
    url='https://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/'
    url+='{country}/{currency}/{locale}?query={query}&apiKey={apiKey}'.format(country='ES',currency='EUR',locale='es-ES',query=StrPlaceName,apiKey='ra66933236979928')
    response = requests.request("GET", url)
    responseJSON=response.json()
    lugares=responseJSON['Places']
    return lugares[0]['PlaceId']

print(FindAirport("Madrid"))


"""
Encuentra las opciones de vuelos segun los parametros deseados mediante la API REST.

"""
def getFlights(headers,originplace,destinationplace,date,nadults,nchildren,ninfants):
  

  data = {
    'cabinclass': 'Economy',
    'country': 'ES',
    'currency': 'EUR',
    'locale': 'es-ES',
    'locationSchema': 'iata',
    'originplace': '{origin}'.format(origin=originplace),
    'destinationplace': '{destination}'.format(destination=destinationplace),
    'outbounddate': '{y}-{m}-{d}'.format(y=str(date.year),m=str(date.month).zfill(2),d=str(date.day).zfill(2)),
    'inbounddate':'',

    'adults': '{numadul}'.format(numadul=nadults),
    'children': '{numchildren}'.format(numchildren=nchildren),
    'infants': '{numinfants}'.format(numinfants=ninfants),
    'apikey': 'ra66933236979928'
  }
  


  response = requests.post('https://partners.api.skyscanner.net/apiservices/pricing/v1.0', headers=headers, data=data)

  respuestaDict=response.__dict__ #Obtengo el diccionario para posteriormente encontrar la SessionKey
  CadenaConSessionKey=respuestaDict['headers']['Location']
  posComienzoSessionKey = np.where(np.array(list(CadenaConSessionKey)) == '/')[0][-1]+1
  SessionKey=CadenaConSessionKey[posComienzoSessionKey:]


  response=requests.get('https://partners.api.skyscanner.net/apiservices/pricing/v1.0/{SessionKey}?apiKey=ra66933236979928'.format(SessionKey=SessionKey))
  Json=(response.json())
  for itinerary in Json['Itineraries']:
    print('OutboundLegId '+itinerary['OutboundLegId'])

    #print('InboundLegId'+itinerary['InboundLegId'])
    PricingOptions=itinerary['PricingOptions']
    print(PricingOptions[0]['Price']) #La opción más barata es la primera opción devuelta
    



headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

def getFlightDetails(headers,OutboundLegId):
  data = {
    'OutboundLegId': '{ID}'.format(ID=OutboundLegId),
  }
  print(data)

  response = requests.put('https://partners.api.skyscanner.net/apiservices/pricing/v1.0/%20%7BSessionKey%7D/booking&apikey=ra66933236979928', headers=headers, data=data)
  print(response.json())



getFlights(headers,"MAD-sky","BCN-sky",dt(2021,3,30),1,0,0)

getFlightDetails(headers,'13870-2103300600--32132-1-9772-2103301235')