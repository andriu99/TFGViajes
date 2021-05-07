
def getProvinceLocationThroughCoordinates(response):
    json=response.json()
    directionData=json['results'][0]['address_components']
    location='Unknown'
    province='Unknown'
    for i in directionData:
        typesList=list(i['types'])
        if typesList.__contains__('locality'):
            location=i['long_name']

        if typesList.__contains__('administrative_area_level_2'):
            province=i['long_name']
    
    return location,province
