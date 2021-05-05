import csv
import requests
import urllib.parse
from app.models import Node


# # Se crea un objeto que abre el fichero y representa su contenido
csvfile = open('stationsData.txt', 'r',encoding='utf-8')
# # Se crea un objeto que formatea el contenido como CSV
reader = csv.reader(csvfile, delimiter=';')


# # Se accede a cada registro del fichero
for fila in reader:
    if fila[8]=='ES':
            
        try:
            latitude=fila[5]
            longitude=fila[6]
            name=fila[1]
            Id=fila[0]
            if latitude=='' or longitude=='' or name=='' or Id=='':
                url='https://www.trainline.eu/api/v5/stations?context=search'
                url+='&q={Place}'.format(Place=urllib.parse.quote(fila[1]))
                postform=requests.get(url)
                jsonEstaciones=postform.json()
                Id=(jsonEstaciones['stations'][0]['id'])
                latitude=(jsonEstaciones['stations'][0]['latitude'])
                longitude=(jsonEstaciones['stations'][0]['longitude'])
            
            new_node=Node(name,Id,latitude,longitude)
            new_node.save()
                
        except:
            print("Error en: "+fila[1])


# # Se cierra el fichero de lectura
csvfile.close()