import requests
import json



def FindAirport(StrPlaceName):
    StrCodigoAirport=''
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/ES/EUR/es-ES/"

    querystring = {"query":StrPlaceName}

    headers = {
    'x-rapidapi-key': "38795e84e7mshf59761a9a492beep134ed0jsn0e2f8e5185a6",
    'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    responseJSON=response.json()
    lugares=responseJSON['Places']
    for lugar in lugares:
        if lugar['CountryName']=='España':
            StrCodigoAirport= lugar['PlaceId']
            return StrCodigoAirport
        

print(FindAirport('Madrid'))
print(FindAirport('Barcelona'))
