import requests

def getAirportsData(geoCatalogJson):
  for continent in geoCatalogJson['Continents']:
      if continent['Name']=='Europe':
          for country in continent['Countries']:
              if country['Name']=='Spain':
                  for city in country['Cities']:
                      for airport in city['Airports']:
                          longLat=str(airport['Location']).replace(' ','').split(",")
                          latLong=longLat[::-1]
                          yield airport['Id'],airport['Name'],latLong[0],latLong[1]
    

def getToken(tokenJson):
  return tokenJson