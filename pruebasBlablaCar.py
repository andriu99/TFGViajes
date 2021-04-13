# -*- coding: utf-8 -*-
"""
Consulta de resultados mediante la API-REST de Blablacar

@author: ANDRES
"""
import datetime
from datetime import datetime as dt
import requests
import json
import urllib.parse

"""
Obtenemos la información de los viajes disponibles según coordenadas y fecha
"""
def ResultadosBlablaCar(listcoordSalida,listcoordLLegada,start_date):
    end_date_local=start_date+datetime.timedelta(days=1)
    url='https://public-api.blablacar.com/api/v3/trips'
    
    start_date_string=start_date.isoformat()
    end_date_string=end_date_local.isoformat()
    params = (
    ('key', 'UIbM2vkhEdrrTLiLnrQkBqgPxrv7S4mI'),
    ('from_coordinate', '{latitudSalida},{longitudSalida}'.format(latitudSalida=listcoordSalida[0],longitudSalida=listcoordSalida[1])),
    ('to_coordinate', '{latitudLlegada},{longitudLlegada}'.format(latitudLlegada=listcoordLLegada[0],longitudLlegada=listcoordLLegada[1])),
    ('currency', 'EUR'),
    ('start_date_local', start_date_string),
    ('end_date_local', end_date_string),
    #('from_cursor','cGFnZT0xOA=='),
    )
    print(params)
    response = requests.get(url, params=params)
    if response.status_code==200:
        print(response.json())
        return response.json()

        
    return ''

"""
Devolvemos el link, los detalles (hora, lugar, coordenadas), y precio de cada viaje encontrado.

"""
def ProcesaJsonBlablaCar(response_json):
    for trip in response_json['trips']:
            yield trip['link'],trip['waypoints'][0],trip['waypoints'][1],trip['price']['amount']
    
            

  

if __name__=="__main__":
    fecha=dt(2021,4,15)
    json=ResultadosBlablaCar(['41.3887900','2.1589900'],['40.416775','-3.703791'],fecha)
    for link,salida,llegada,precio in ProcesaJsonBlablaCar(json):
        print(link,salida,llegada,precio)