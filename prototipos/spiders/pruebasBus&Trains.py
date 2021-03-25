
import json
import requests
from datetime import datetime as dt

def getPlaceStations(Place):
    url='https://www.trainline.eu/api/v5/stations?context=search'
    url+='&q={Place}'.format(Place=Place)

    postform=requests.get(url)

    print(postform.json())
    for station in postform.json()['stations']:
      print(station['id'])
      print(station['name'])
      print(station['latitude'])
      print(station['longitude'])
    


#print(getPlaceStations("Madrid"))
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
      "systems":["busbud"] #Busbud o Renfe
    }
}

def BuscaTrips(system,departure_station_id,arrival_station_id,departure_date):
  body['search']['systems']=[system]
  body['search']['departure_station_id']=departure_station_id
  body['search']['arrival_station_id']=arrival_station_id
  body['search']['departure_date']=departure_date
  print(body)
  try:  
    response=requests.post(url,headers=headers,data=json.dumps(body))
    for trip in response.json()['trips']:
      print(trip['cents'])
      print(trip['departure_date'])
      print(trip['arrival_date'])
      print('\n')

  except Exception:
    print("hola")
    
  


fechaprueba=dt(2021,3,29)
BuscaTrips("renfe",33349,9627,fechaprueba.isoformat())
