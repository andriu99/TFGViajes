import requests
params={
    'apiKey':'prtl6749387986743898559646983194'
}
response=requests.get('https://partners.api.skyscanner.net/apiservices/geo/v1.0',params=params,timeout=None)
#numContinente=np.where(np.array(response.json()['Continents']))
for continent in response.json()['Continents']:
    if continent['Name']=='Europe':
        for country in continent['Countries']:
            if country['Name']=='Spain':
                for city in country['Cities']:
                    for airport in city['Airports']:
                        print(airport['Id'])
                        print(airport['Name'])
                        longLat=str(airport['Location']).replace(' ','').split(",")
                        print(longLat[1],longLat[0])

                        
