
def getStationInformation(response):
    json=response.json()
    Id=json['stations'][0]['id']
    latitud=json['stations'][0]['latitude']
    longitud=json['stations'][0]['longitude']
    return Id,latitud,longitud


def findbustrainTrips(response):
    try:
        for trip in response.json()['trips']:
            yield trip['cents']/100,trip['departure_date'],trip['arrival_date']
    except:
        return None 
