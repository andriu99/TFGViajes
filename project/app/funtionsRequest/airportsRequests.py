import numpy as np


def getTokenOrFlightData(response):
    return response.json()

def getAirportID(response):
    responseJSON=response.json()
    lugares=responseJSON['Places']
    return lugares[0]['PlaceId']

def getSessionKey(response):
    respuestaDict=response.__dict__ #Obtengo el diccionario para posteriormente encontrar la SessionKey
    CadenaConSessionKey=respuestaDict['headers']['Location']
    posComienzoSessionKey = np.where(np.array(list(CadenaConSessionKey)) == '/')[0][-1]+1 #Encuentra la posición del último / de la cadena
    SessionKey=CadenaConSessionKey[posComienzoSessionKey:] #La Session Key será desde la última / hasta el final

    return SessionKey

def getFlightInformation(response):
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