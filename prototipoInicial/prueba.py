url='https://www.trainline.eu/api/v5/stations?context=search'
params={
    'q':"Burgos"
}
import requests
response=requests.get(url,params=params)
print(response.json())