
def findBlablaTrips(response):
    print(response)
    jsonBlabla=response.json()
    for trip in jsonBlabla['trips']:
            yield trip['link'],trip['waypoints'][0],trip['waypoints'][1],trip['price']['amount']