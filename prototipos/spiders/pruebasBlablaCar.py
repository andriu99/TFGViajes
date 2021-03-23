# -*- coding: utf-8 -*-
"""
Consulta de resultados mediante la API-REST de Blablacar

@author: ANDRES
"""
import datetime
from datetime import datetime as dt
import requests
import json

"""
Obtenemos la información de los viajes disponibles según coordenadas y fecha
"""
def ResultadosBlablaCar(listcoordSalida,listcoordLLegada,start_date):
    end_date_local=start_date+datetime.timedelta(days=1)
    url='https://public-api.blablacar.com/api/v3/trips?key=UIbM2vkhEdrrTLiLnrQkBqgPxrv7S4mI'
    
    start_date_string=start_date.isoformat()
    end_date_string=end_date_local.isoformat()
   
    #Añado las coordenadas:
    url+='&from_coordinate={latitudSalida},{longitudSalida}&to_coordinate={latitudLlegada},{longitudLlegada}'.format(latitudSalida=listcoordSalida[0],longitudSalida=listcoordSalida[1],latitudLlegada=listcoordLLegada[0],longitudLlegada=listcoordLLegada[1])
    #Añado la opción de moneda (euros)
    url+='&currency=EUR'
    #Añado las fechas maxima y minima:
    url+='&start_date_local={}&end_date_local={}'.format(start_date_string,end_date_string)   
    
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
    
            

  


# fecha=dt(2021,3,20)
# json=ResultadosBlablaCar(['41.3887900','2.1589900'],['40.416775','-3.703791'],fecha)
# for i in ProcesaJsonBlablaCar(json):
#     print(i)