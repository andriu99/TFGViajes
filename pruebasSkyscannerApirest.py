import requests
import numpy as np
import json
from datetime import datetime as dt
import urllib.parse
"""
Encuentra el código del aeropuerto de la ciudad deseada vía API-REST
"""
def FindAirport(token,StrPlaceName):
    print(token.json())
    params = (
      ('query',StrPlaceName),
      ('apiKey',token.json()),
    )
    response = requests.get('https://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/ES/EUR/es-ES', params=params)
    print(response.text)
    # print(response.url)
    # url='https://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/'
    # url+='{country}/{currency}/{locale}?query={query}&apiKey={apiKey}'.format(country='ES',currency='EUR',locale='es-ES',query=StrPlaceName,apiKey=token)
      # response = requests.request("GET", url)
    responseJSON=response.json()
    lugares=responseJSON['Places']
    return lugares[0]['PlaceId']

"""
Obtengo el Json con la información de los vuelos según los parámetros dados
"""
def getJson(headers,data):
  print(data)
  session=requests.Session()

  response = session.post('https://partners.api.skyscanner.net/apiservices/pricing/v1.0', headers=headers, data=data)
  respuestaDict=response.__dict__ #Obtengo el diccionario para posteriormente encontrar la SessionKey
  print(respuestaDict)
  CadenaConSessionKey=respuestaDict['headers']['Location']
  posComienzoSessionKey = np.where(np.array(list(CadenaConSessionKey)) == '/')[0][-1]+1 #Encuentra la posición del último / de la cadena
  SessionKey=CadenaConSessionKey[posComienzoSessionKey:] #La Session Key será desde la última / hasta el final
  params={
      'stops':0, #Sólo busco vuelos directos
  }
  response=session.get('https://partners.api.skyscanner.net/apiservices/pricing/v1.0/{SK}?apiKey={token}'.format(SK=SessionKey,token=data['apikey']),params=params)

  return response.json()

"""
Encuentra las opciones de vuelos segun los parametros deseados mediante la API REST.
"""
def getFlights(token,headers,originplace,destinationplace,date,nadults,nchildren,ninfants):

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
      'apikey': '{key}'.format(key=token.json())

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
  token=requests.get("https://partners.api.skyscanner.net/apiservices/token/v2/gettoken?apiKey=prtl6749387986743898559646983194")
  #token=urllib.parse.quote(token.json())
  print(token)
  headers = {
      'Content-Type': 'application/x-www-form-urlencoded',

  }

  print(FindAirport(token,"Burgos"))
  FlightGenerator=(getFlights(token,headers,"MAD-sky","BCN-sky",dt(2021,4,20),1,0,0))
  for Precio,UrlPago,FechaSalida,FechaLlegada,Duracion,AirlineName,AirlineUrlImage in FlightGenerator:
    print(Precio,FechaSalida,FechaLlegada,Duracion,AirlineName,AirlineUrlImage)