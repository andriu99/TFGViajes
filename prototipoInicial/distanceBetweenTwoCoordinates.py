from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


d=haversine(40.4043078,-3.6896317615447,41.37901205,2.13996016646417)
print(d)
url='https://maps.googleapis.com/maps/api/distancematrix/json'
params={
    'origins':'40.4043078,-3.6896317615447',
    'destinations':'41.37901205,2.13996016646417',
    'key':'AIzaSyCaR0xc4Xiv3rHEV-HkFD-4Dt7hsIx3aT0',
    'avoid':'tolls'
}

import requests
rq=requests.get(url,params=params)
print(rq.json())