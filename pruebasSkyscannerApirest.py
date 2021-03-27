import requests
import numpy as np
import json
from datetime import datetime as dt
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

"""
Obtengo el Json con la información de los vuelos según los parámetros dados
"""
def getJson(headers,data):
  response = requests.post('https://partners.api.skyscanner.net/apiservices/pricing/v1.0', headers=headers, data=data)
  respuestaDict=response.__dict__ #Obtengo el diccionario para posteriormente encontrar la SessionKey
  CadenaConSessionKey=respuestaDict['headers']['Location']
  posComienzoSessionKey = np.where(np.array(list(CadenaConSessionKey)) == '/')[0][-1]+1 #Encuentra la posición del último / de la cadena
  SessionKey=CadenaConSessionKey[posComienzoSessionKey:] #La Session Key será desde la última / hasta el final
  params={
      'stops':0, #Sólo busco vuelos directos
  }
  response=requests.get('https://partners.api.skyscanner.net/apiservices/pricing/v1.0/{SK}?apiKey=ra66933236979928'.format(SK=SessionKey),params=params)
  return response.json()

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
  Json=getJson(headers,data)
  
  ItinerariosJson=Json['Itineraries']
  DetailsJson=Json['Legs']
  AirlinesJson=Json['Carriers']
  for itinerary,details,airline in zip(ItinerariosJson,DetailsJson,AirlinesJson):
    Precio=itinerary['PricingOptions'][0]['Price']
    UrlPago=itinerary['PricingOptions'][0]['DeeplinkUrl']
    FechaSalida=details['Departure']
    FechaLlegada=details['Arrival']
    Duracion=details['Duration']
    AirlineName=airline['Name']
    AirlineUrlImage=airline['ImageUrl']
    yield Precio,UrlPago,FechaSalida,FechaLlegada,Duracion,AirlineName,AirlineUrlImage



if __name__=="__main__":
  
  headers = {
      'Content-Type': 'application/x-www-form-urlencoded',

  }
  FlightGenerator=(getFlights(headers,"MAD-sky","BCN-sky",dt(2021,3,30),1,0,0))
  for Precio,UrlPago,FechaSalida,FechaLlegada,Duracion,AirlineName,AirlineUrlImage in FlightGenerator:
    print(Precio,FechaSalida,FechaLlegada,Duracion,AirlineName,AirlineUrlImage)