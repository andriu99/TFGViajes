

import csv
import urllib.parse
from app.models import Node,Request
import os
from app.funtionsRequest.googleMapsRequests import get_locat_province

def run():
    workpath = os.path.dirname(os.path.abspath(__file__)) #Returns the Path your .py file is in
    getStationInformation=Request.objects.get(name='getStationInformationTrainline')

    # # Se crea un objeto que abre el fichero y representa su contenido
    csvfile = open(os.path.join(workpath, 'stationsData.txt'), 'r',encoding='utf-8')
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
                    jsonEstaciones=getStationInformation('{Place}'.format(Place=urllib.parse.quote(fila[1])))
                    Id=jsonEstaciones['stations'][0]['id']
                    latitude=jsonEstaciones['stations'][0]['latitude']
                    longitude=jsonEstaciones['stations'][0]['longitude']
                
                address,location,province=get_locat_province(str(latitude)+','+str(longitude),True)
                

                new_node=Node(address=address,name=name,code=Id,latitude=float(latitude),longitude=float(longitude),nodeType='S',location=location,province=province)
                new_node.save()
            except:
                print("Error en: "+fila[1])
    csvfile.close()
