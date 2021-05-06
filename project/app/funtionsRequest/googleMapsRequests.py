
def getProvinceLocationThroughCoordinates(response):
    json=response.json()
    for i in (json['results'][0]['address_components']):
        if list(i['types']).__contains__('locality'):
            location=i['long_name']

        if list(i['types']).__contains__('administrative_area_level_2'):
            province=i['long_name']

    return location,province
