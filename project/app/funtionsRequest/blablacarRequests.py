
def findBlablaTrips(response):
    jsonBlabla=response.json()
    for trip in jsonBlabla['trips']:
        startData=trip['waypoints'][0]
        endData=trip['waypoints'][1]
        yield (trip['link'],
               startData['date_time'],startData['place']['city'],startData['place']['address'],startData['place']['latitude'],startData['place']['longitude'],
               endData['date_time'],endData['place']['city'],endData['place']['address'],endData['place']['latitude'],endData['place']['longitude'],
               trip['price']['amount']
        )