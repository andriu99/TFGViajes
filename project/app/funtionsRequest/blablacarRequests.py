
def findBlablaTrips(response):
    for trip in response.json()['trips']:
            yield trip['link'],trip['waypoints'][0],trip['waypoints'][1],trip['price']['amount']