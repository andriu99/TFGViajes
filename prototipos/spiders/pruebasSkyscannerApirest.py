import requests
import urllib.parse
import numpy as np
import json
# response = requests.request("GET", 'https://partners.api.skyscanner.net/apiservices/token/v2/gettoken?apiKey={apiKey}'.format(apiKey='ra66933236979928'))


# token=response.text
# print(urllib.parse.quote(token))
"""
Encuentra el código del aeropuerto vía API-REST
"""
def FindAirport(StrPlaceName):
    url='https://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/'
    url+='{country}/{currency}/{locale}?query={query}&apiKey={apiKey}'.format(country='ES',currency='EUR',locale='es-ES',query=StrPlaceName,apiKey='ra66933236979928')
    response = requests.request("GET", url)
    responseJSON=response.json()
    lugares=responseJSON['Places']
    return lugares[0]['CityId']

print(FindAirport("Madrid"))


headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
  #'cabinclass': 'Economy',
  'country': 'ES',
  'currency': 'EUR',
  'locale': 'es-ES',
  'locationSchema': 'iata',
  'originplace': 'MADR-sky',
  'destinationplace': 'BARC-sky',
  'outbounddate': '2021-03-30',
  'inbounddate':'',

  'adults': '1 ',
  'children': '0 ',
  'infants': '0 ',
  'apikey': 'ra66933236979928'
}

response = requests.post('https://partners.api.skyscanner.net/apiservices/pricing/v1.0', headers=headers, data=data)
respuestaDict=response.__dict__
CadenaConSessionKey=respuestaDict['headers']['Location']
posComienzoSessionKey = np.where(np.array(list(CadenaConSessionKey)) == '/')[0][-1]+1
SessionKey=CadenaConSessionKey[posComienzoSessionKey:]


response=requests.get('https://partners.api.skyscanner.net/apiservices/pricing/v1.0/{SessionKey}?apiKey=ra66933236979928'.format(SessionKey=SessionKey))
Json=(response.json())
for itinerary in Json['Itineraries']:
  PricingOptions=itinerary['PricingOptions']
  Price=PricingOptions[0]['Price']
  print(PricingOptions[0]['Price'])
 