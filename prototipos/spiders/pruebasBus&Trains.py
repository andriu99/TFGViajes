
import json
import requests
from datetime import datetime as dt

def getPlaceStations(Place):
    url='https://www.trainline.eu/api/v5/stations?context=search'
    url+='&q={Place}'.format(Place=Place)

    postform=requests.get(url)
    print(postform.json())
    


print(getPlaceStations("Madrid"))
print(getPlaceStations("Burgos"))

url='https://www.trainline.eu/api/v5_1/search'
headers = {
    'Accept': 'application/json',
    'User-Agent': 'CaptainTrain/5221(d109181b0) (iPhone8,4; iOS 13.1.2; Scale/2.00)',
    'Accept-Language': 'es',
    'Content-Type': 'application/json; charset=UTF-8',
    'Host': 'www.trainline.eu',
    'authorization': 'Token token="A8fQLJDF94cPUKEu3Vpi"',
}

body = {
  
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
      "systems":["busbud"]
    }
}
#alfkdjs
#      "systems":["sncf","db","busbud","idtgv","ouigo","trenitalia","ntv","hkx","renfe","timetable"]

#2021-03-27T22:00:00
#print(json.dumps(body))
response=requests.post(url,headers=headers,data=json.dumps(body))
print(dt.now().isoformat())
Json=(response.json())
for i in response.json():
  print(i)


for trip in Json['trips']:
  print(trip['cents'])
  print(trip['departure_date'])
  print(trip['arrival_date'])
  print('\n')
