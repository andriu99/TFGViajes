from app.models import Request,RESTApi
import json

def run():
  importGoogleMapsInfo()
  importBlablacarInfo()
  importSkyscannerInfo()
  importTrainlineInfo()


def importGoogleMapsInfo():
  googleMapsRESTApi=RESTApi(name='googleMapsRESTApi',BaseUrl='https://maps.googleapis.com/maps/',APIKey='AIzaSyAi0WZL0uYN3vT__dfLObTB67XAaFRUIY4')
  googleMapsRESTApi.save()
  



def importBlablacarInfo():
  blablaCarRESTApi=RESTApi(name='BlablaCarRESTApi',BaseUrl='https://public-api.blablacar.com',APIKey='UIbM2vkhEdrrTLiLnrQkBqgPxrv7S4mI')
  blablaCarRESTApi.save()
  paramsblabla={
      "key": "example", 
      "currency": "EUR", 

      "from_coordinate": "41.3887900,2.1589900", 
      "to_coordinate": "40.416775,-3.703791", 
      "start_date_local": "2021-05-05T00:00:00", 
      "end_date_local": "2021-05-06T00:00:00"
      }

  findBlablaTrips=Request(name='getBlablaCarTrips',description='Find blablacar´s trips with dates and coordinates',PartToaddToBaseUrl='/api/v3/trips',
                          funcToExtractDataFromJsonName='findBlablaTrips',ParamsOrDataDictStructure=json.dumps(paramsblabla),typeRequests='GET',RApi=blablaCarRESTApi)

  findBlablaTrips.save()


def importSkyscannerInfo():
  
  skyscannerRESTApi=RESTApi(name='SkyscannerRESTApi',BaseUrl='https://partners.api.skyscanner.net/apiservices/',APIKey='prtl6749387986743898559646983194')
  skyscannerRESTApi.save()
  paramsGetSkyscToken={
      'apiKey':'example',
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

  getToken=Request(name='getTokenSkyscanner',description='Get a token with the API-key',PartToaddToBaseUrl='token/v2/gettoken',
                   funcToExtractDataFromJsonName='getTokenOrFlightData',ParamsOrDataDictStructure=json.dumps(paramsGetSkyscToken),typeRequests='GET',RApi=skyscannerRESTApi)

  getSessionKey=Request(name='getSessionKeySkyscanner',description='Get the session key',PartToaddToBaseUrl='pricing/v1.0',
                        funcToExtractDataFromJsonName='getSessionKey',ParamsOrDataDictStructure=json.dumps(datagetSessionKey),typeRequests='POST',headers={'Content-Type': 'application/x-www-form-urlencoded'},RApi=skyscannerRESTApi)

  getFlightsInformation=Request(name='getFlightsInformationSkyscanner',description='Get information about flights',PartToaddToBaseUrl='pricing/v1.0/',
                                funcToExtractDataFromJsonName='getFlightInformation',ParamsOrDataDictStructure=json.dumps(getFlightInformationparams),typeRequests='GET',RApi=skyscannerRESTApi)##

  getGeoCatalogInformation=Request(name='getSkyscannerGeocatalog',description='Get information about airports',PartToaddToBaseUrl='geo/v1.0',
                                  funcToExtractDataFromJsonName='getAirportsData',ParamsOrDataDictStructure=json.dumps(getGeoCatalogparams),typeRequests='GET',RApi=skyscannerRESTApi)

  getToken.save()
  getSessionKey.save()
  getFlightsInformation.save()
  getGeoCatalogInformation.save()


def importTrainlineInfo():
  trainlineRESTApi=RESTApi(name='TrainlineRESTApi',BaseUrl='https://www.trainline.eu/api/v5_1/',APIKey='A8fQLJDF94cPUKEu3Vpi')
  trainlineRESTApi.save()
  paramsgetStation={
      'q':'Place',
  }
  getStationInformation=Request(name='getStationInformationTrainline',description='Get information about a station',PartToaddToBaseUrl='stations?context=search',
                                funcToExtractDataFromJsonName='getStationInformation',ParamsOrDataDictStructure=json.dumps(paramsgetStation),typeRequests='GET',RApi=trainlineRESTApi)

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

  getbustrainTripsInformation=Request(name='getbustrainTripsInformationTrainline',description='Get trips information by train or bus',PartToaddToBaseUrl='search',
                                      funcToExtractDataFromJsonName='findbustrainTrips',ParamsOrDataDictStructure=json.dumps(dataFindTrip),typeRequests='POST',headers=headersTrainline,RApi=trainlineRESTApi)
  getStationInformation.save()
  getbustrainTripsInformation.save()







