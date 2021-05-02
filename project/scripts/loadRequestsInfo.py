import csv
from app.models import Request,RESTApi,Node

 #$ python manage.py runscript example


blablaCarRESTApi=RESTApi('BlablaCarRESTApi','https://public-api.blablacar.com','UIbM2vkhEdrrTLiLnrQkBqgPxrv7S4mI')
blablaCarRESTApi.save()
paramsblabla={
    'key': 'example', 
    'from_coordinate': '41.3887900,2.1589900', 
    'to_coordinate': '40.416775,-3.703791', 
    'currency': 'EUR', 
    'start_date_local': '2021-05-05T00:00:00', 
    'end_date_local': '2021-05-06T00:00:00'
    }

findBlablaTrips=Request('BlablaRequest','Find blablacar´s trips with dates and coordinates','/api/v3/trips','findBlablaTrips',paramsblabla,'GET',RApi=blablaCarRESTApi)
findBlablaTrips.save()



skyscannerRESTApi=RESTApi('SkyscannerRESTApi','https://partners.api.skyscanner.net/apiservices/','prtl6749387986743898559646983194')
skyscannerRESTApi.save()
paramsGetSkyscToken={
    'apiKey':'prtl6749387986743898559646983194',
}

paramsFindAirport={
    'query': 'Burgos',
    'apiKey': 'example'
}

datagetSessionKey={
      'cabinclass': 'Economy',
      'country': 'ES',
      'currency': 'EUR',
      'locale': 'es-ES',
      'locationSchema': 'iata',
      'originplace': 'origin',
      'destinationplace': 'destination',
      'outbounddate': 'outbounddate',
      'adults': '1',
      'children': '0',
      'infants': '0',
      'apikey': 'example'

}

getFlightInformationparams={
      'stops':0, #Sólo busco vuelos directos
      'apiKey':'token',
}

getGeoCatalogparams={
  'apiKey':'token',
}

getToken=Request('getToken','Get a token with the API-key','token/v2/gettoken','getTokenOrFlightData',paramsGetSkyscToken,'GET',RApi=skyscannerRESTApi)
#findAirport=Request('getAirportID','Find an airport ID','autosuggest/v1.0/ES/EUR/es-ES','getAirportID',paramsFindAirport,'GET',RApi=skyscannerRESTApi)
getSessionKey=Request('getSessionKey','Get the session key','pricing/v1.0','getSessionKey',datagetSessionKey,'POST',headers={'Content-Type': 'application/x-www-form-urlencoded'},RApi=skyscannerRESTApi)
getFlightsInformation=Request('getFlightsInformation','Get information about flights','pricing/v1.0/',getFlightInformationparams,'GET',RApi=skyscannerRESTApi)##
getGeoCatalogInformation=Request('getGeoCatalogInformation','Get information about airports','geo/v1.0',getGeoCatalogparams,'GET',RApi=skyscannerRESTApi)

getToken.save()
#findAirport.save()
getSessionKey.save()
getFlightsInformation.save()



trainlineRESTApi=RESTApi('TrainlineRESTApi','https://www.trainline.eu/api/v5_1/','A8fQLJDF94cPUKEu3Vpi')
trainlineRESTApi.save()
paramsgetStation={
    'q':'Place',
}
getStationInformation=Request('getStationInformation','Get information about a station','stations?context=search','getStationInformation',paramsgetStation,'GET',RApi=trainlineRESTApi)

dataFindTrip = {
  
    "local_currency": "EUR",
    "search": {
      "passenger_ids": [
        "314892886"
      ],
      "card_ids": [
        "14127110"
      ],
      "departure_station_id":33349,
      "arrival_station_id":6627,
      "departure_date":"2021-03-29T00:00:00+01:00",
      "systems":[]
    }
}

headersTrainline = {
    'Accept': 'application/json',
    'User-Agent': 'CaptainTrain/5221(d109181b0) (iPhone8,4; iOS 13.1.2; Scale/2.00)',
    'Accept-Language': 'es',
    'Content-Type': 'application/json; charset=UTF-8',
    'Host': 'www.trainline.eu',
    'authorization': 'Token token="{token}"'.format(token=trainlineRESTApi.APIKey),
}

getbustrainTripsInformation=Request('getbustrainTripsInformation','Get trips information by train or bus','search','findbustrainTrips',dataFindTrip,'POST',headers=headersTrainline,RApi=trainlineRESTApi)
getStationInformation.save()
getbustrainTripsInformation.save()