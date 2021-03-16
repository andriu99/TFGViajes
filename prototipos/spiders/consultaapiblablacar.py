# -*- coding: utf-8 -*-
"""
Consulta de resultados mediante la API-REST de Blablacar

@author: ANDRES
"""
import datetime
from datetime import datetime as dt
import requests

"""
Obtenemos la información de los viajes disponibles según coordenadas y fecha
"""
def ResultadosBlablaCar(listcoordSalida,listcoordLLegada,start_date):
    end_date_local=start_date+datetime.timedelta(days=1)
    url='https://public-api.blablacar.com/api/v3/trips?key=UIbM2vkhEdrrTLiLnrQkBqgPxrv7S4mI'
    #Añado las coordenadas:
    url+='&from_coordinate='+listcoordSalida[0]+','+listcoordSalida[1]+'&to_coordinate='+listcoordLLegada[0]+','+listcoordLLegada[1]
    #Añado la opción de moneda (euros)
    url+='&currency=EUR'
    #Añado las fechas maxima y minima:
    url+='&start_date_local='+str(start_date.isoformat())+'&end_date_local='+str(end_date_local.isoformat())

    response=requests.get(url)
    if response.status_code==200:
        return response.json()

        
    return ''

"""
Devolvemos el link, los detalles (hora, lugar, coordenadas), y precio de cada viaje encontrado.

"""
def ProcesaJsonBlablaCar(response_json):
    for trip in response_json['trips']:
            yield trip['link'],trip['waypoints'][0],trip['waypoints'][1],trip['price']['amount']
    
            

  


fecha=dt(2021,3,14)
json=ResultadosBlablaCar(['41.3887900','2.1589900'],['40.416775','-3.703791'],fecha)
