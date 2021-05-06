import requests
url='https://maps.googleapis.com/maps/api/geocode/json'
params={'latlng': '43.302778,-2.921667', 'key': 'AIzaSyCaR0xc4Xiv3rHEV-HkFD-4Dt7hsIx3aT0'}

json=requests.get(url,params=params).json()
for i in (json['results'][0]['address_components']):
    print(i)
    if list(i['types']).__contains__('locality'):
        location=(i['long_name'])

    if list(i['types']).__contains__('administrative_area_level_2'):
        province=(i['long_name'])

print(location)
print(province)
