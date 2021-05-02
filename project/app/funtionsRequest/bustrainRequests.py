
def getStationInformation(response):
    json=response.json()
    Id=json['stations'][0]['id']
    latitud=json['stations'][0]['latitude']
    longitud=json['stations'][0]['longitude']
    return Id,latitud,longitud


def findbustrainTrips(response):
    for trip in response.json()['trips']:
      yield trip['cents'],trip['departure_date'],trip['arrival_date']
