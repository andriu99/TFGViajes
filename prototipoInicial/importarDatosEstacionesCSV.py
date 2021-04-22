import csv
import requests
import urllib.parse


# # Se crea un objeto que abre el fichero y representa su contenido
csvfile = open('datos.txt', 'r',encoding='utf-8')
# # Se crea un objeto que formatea el contenido como CSV
reader = csv.reader(csvfile, delimiter=';')


# # Se accede a cada registro del fichero
for fila in reader:
    if fila[8]=='ES':
            
        try:
            latitud=fila[5]
            longitud=fila[6]
            name=fila[1]
            Id=fila[0]
            if latitud=='' or longitud=='' or name=='' or Id=='':
                url='https://www.trainline.eu/api/v5/stations?context=search'
                url+='&q={Place}'.format(Place=urllib.parse.quote(fila[1]))
                postform=requests.get(url)
                jsonEstaciones=postform.json()
                Id=(jsonEstaciones['stations'][0]['id'])
                latitud=(jsonEstaciones['stations'][0]['latitude'])
                longitud=(jsonEstaciones['stations'][0]['longitude'])
                    
            with open("stationsSpain.txt", 'a+', newline = '',encoding='utf-8') as outfile:
                csv_writer = csv.writer(outfile, delimiter = ',')
                csv_writer.writerow([Id,name,latitud,longitud])

                
        except:
            print("Error en: "+fila[1])


# # Se cierra el fichero de lectura
csvfile.close()
