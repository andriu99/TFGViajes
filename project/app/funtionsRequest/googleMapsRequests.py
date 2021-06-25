
from ..models import RESTApi
import time
import googlemaps as gmaps
from pytz import timezone
import timezonefinder


def get_province_muni_json(response_json,required_address=False):
   
    directionData=response_json[0]['address_components']

    location='Unknown'
    province='Unknown'
    for i in directionData:
        typesList=list(i['types'])
        if typesList.__contains__('locality'):
            location=i['long_name']

        if typesList.__contains__('administrative_area_level_2'):
            province=i['long_name']
    
    if required_address:
        return response_json[0]['formatted_address'],location,province
    return location,province



def getTime_between_coordinates(coordinates_origin,coordinates_destination):
    ClientGMaps=gmaps.Client(RESTApi.objects.get(name='googleMapsRESTApi').APIKey)
    resultJson=ClientGMaps.distance_matrix(origins=coordinates_origin,destinations=coordinates_destination)
        
    return resultJson['rows'][0]['elements'][0]['duration']['value']



def parseDate_withTimeZone(date_date,lat,lon):
   
    tf = timezonefinder.TimezoneFinder()

    timezone_str = tf.certain_timezone_at(lat=lat, lng=lon)
    date_date=date_date.astimezone(timezone(timezone_str))
    return date_date



def get_locat_province(coordinates,required_address=False):
    
    ClientGMaps=gmaps.Client(RESTApi.objects.get(name='googleMapsRESTApi').APIKey)
    x=3
    while x>0:
        try:
            if required_address:
               
                address,location,province=get_province_muni_json(ClientGMaps.reverse_geocode(coordinates),required_address)
                return address,location,province

            else:
                location,province=get_province_muni_json(ClientGMaps.reverse_geocode(coordinates),required_address)
                return location,province
            
        except:
            time.sleep(0.02)
        x-=1

    if required_address:
        return 'Unknown','Unknown','Unknown'

    return 'Unknown','Unknown'
