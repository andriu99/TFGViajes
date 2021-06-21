import numpy as np
import time
import random
def getAirportsData(response):
  geoCatalogJson=response.json()
  for continent in geoCatalogJson['Continents']:
      if continent['Name']=='Europe':
          for country in continent['Countries']:
              if country['Name']=='Spain':
                  for city in country['Cities']:
                      for airport in city['Airports']:
                          longLat=str(airport['Location']).replace(' ','').split(",")
                          latLong=longLat[::-1]
                          yield airport['Id'],airport['Name'],latLong[0],latLong[1]

    
def getTokenOrFlightData(response):
    return response.json()

def getAirportID(response):
    responseJSON=response.json()
    lugares=responseJSON['Places']
    return lugares[0]['PlaceId']

def getSessionKey(response):

    x=3
    while x>0:
        try:
            respuestaDict=response.__dict__ #Obtengo el diccionario para posteriormente encontrar la SessionKey
            CadenaConSessionKey=respuestaDict['headers']['Location']
            posComienzoSessionKey = np.where(np.array(list(CadenaConSessionKey)) == '/')[0][-1]+1 #Encuentra la posición del último / de la cadena
            SessionKey=CadenaConSessionKey[posComienzoSessionKey:] #La Session Key será desde la última / hasta el final
            break
        except:
            time.sleep(random.randint(0,10))

        x-=1
    return SessionKey

def getFlightInformation(response):
    try:

        Json=response.json()
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

    except:
        return None