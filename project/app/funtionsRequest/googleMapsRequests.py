
def getProvinceLocationThroughCoordinates(response_json):
    try: #Request
        json=response_json.json()
        directionData=json['results'][0]['address_components']
    except: #JSON
        directionData=response_json[0]['address_components']

    
        
  
    location='Unknown'
    province='Unknown'
    for i in directionData:
        typesList=list(i['types'])
        if typesList.__contains__('locality'):
            location=i['long_name']

        if typesList.__contains__('administrative_area_level_2'):
            province=i['long_name']
    
    return location,province


def getTimeZone(response):
    return response.json()['timeZoneId']

def getLatLong_address(json):
    return json[0]['geometry']['location']['lat'],json[0]['geometry']['location']['lng']


def getTime_between_coordinates(json):
    return json['rows'][0]['elements'][0]['duration']['value']
