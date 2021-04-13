
import json
import requests
from datetime import datetime as dt

"""
Nos devuelve id, nombre, latitud y longitud de la estación buscada
"""
def getPlaceStations(Place):
    url='https://www.trainline.eu/api/v5/stations?context=search'
    url+='&q={Place}'.format(Place=Place)

    postform=requests.get(url)

    for station in postform.json()['stations']:
      print(station)
      yield station['id'],station['name'],station['latitude'],station['longitude']
   


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
      "systems":[]
    }
}

"""
Obtenemos precio, fecha de salida y fecha de llegada para cada viaje.
"""
def BuscaTrips(system,departure_station_id,arrival_station_id,departure_date):
  body['search']['systems']=system
  body['search']['departure_station_id']=departure_station_id
  body['search']['arrival_station_id']=arrival_station_id
  body['search']['departure_date']=departure_date
  try:  
    response=requests.post(url,headers=headers,data=json.dumps(body))
    for trip in response.json()['trips']:
      yield trip['cents'],trip['departure_date'],trip['arrival_date']
   
  except Exception:
    print("Fallo")
    
  
if __name__=="__main__":
  for id,name,latitude,longitude in (getPlaceStations("Madrid")):
    print(name,id,latitude,longitude)

  fechaprueba=dt(2021,4,13)
  for price,fechaSal,fechaLlegada in BuscaTrips(["busbud"],6663,24410,fechaprueba.isoformat()):
    print(price,fechaSal,fechaLlegada)
