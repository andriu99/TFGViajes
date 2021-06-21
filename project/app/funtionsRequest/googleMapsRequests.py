
from ..models import RESTApi
import time
import googlemaps as gmaps
from pytz import timezone
import timezonefinder


def get_province_muni_json(response_json):
   
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



def getTime_between_coordinates(coordinates_origin,coordinates_destination):
    ClientGMaps=gmaps.Client(RESTApi.objects.get(name='googleMapsRESTApi').APIKey)
    resultJson=ClientGMaps.distance_matrix(origins=coordinates_origin,destinations=coordinates_destination)
        
    return resultJson['rows'][0]['elements'][0]['duration']['value']



def parseDate_withTimeZone(date_date,lat,lon):
    # ClientGMaps=gmaps.Client(RESTApi.objects.get(name='googleMapsRESTApi').APIKey)

    # dict_location={
    #     "lat" : lat,
    #     "lng" : lon,
  
    # }
    # dict_timezone=ClientGMaps.timezone(dict_location)
    tf = timezonefinder.TimezoneFinder()

    timezone_str = tf.certain_timezone_at(lat=lat, lng=lon)
    date_date=date_date.astimezone(timezone(timezone_str))
    return date_date



def get_locat_province(coordinates):
    
    ClientGMaps=gmaps.Client(RESTApi.objects.get(name='googleMapsRESTApi').APIKey)
    x=3
    while x>0:
        try:
            location,province=get_province_muni_json(ClientGMaps.reverse_geocode(coordinates))
            break
        except:
            time.sleep(0.02)
        x-=1

    return location,province
