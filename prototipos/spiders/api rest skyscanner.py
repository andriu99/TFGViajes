import requests
import json
import datetime
from datetime import datetime as dt
from scrapy.crawler import CrawlerProcess
from scrapy import Request


import scrapy
class scrapySkyscanner(scrapy.Spider):
    name = 'skyscannerspider'
    start_urls = ['https://www.skyscanner.es/transporte/vuelos']

    

    def __init__(self,origin,destination,date):
    
        Strorigen=self.ProcesaString(self.FindAirport(origin))
        Strdestino=self.ProcesaString(self.FindAirport(destination))
        self.start_urls=[self.getUrl(Strorigen,Strdestino,date)]

        
    

    """
    Encuentra el código del aeropuerto vía API-REST
    """
    def FindAirport(self,StrPlaceName):
        url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/ES/EUR/es-ES/"

        querystring = {"query":StrPlaceName}

        headers = {
        'x-rapidapi-key': "38795e84e7mshf59761a9a492beep134ed0jsn0e2f8e5185a6",
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        responseJSON=response.json()
        lugares=responseJSON['Places']
        return lugares[0]['PlaceId']
        
    """
    Convierte la cadena devuelta por la API-REST a una que podemos usar para buscar vía URL.
    """        
    def ProcesaString(self,strAirport):
        codigoAirport=str(strAirport[0:3]).lower()
        return codigoAirport

    """
    Retorna la URL
    """
    def getUrl(self,strAirportStart,strAirportEnd,date):
        url='https://www.skyscanner.es/transporte/vuelos'
        url+='/{startPlace}/{endPlace}/{year}{month}{day}'.format(startPlace=strAirportStart,endPlace=strAirportEnd,year=str(date.year)[2:],month=str(date.month).zfill(2),day=str(date.day).zfill(2))
        return url

    def parse(self,response):

        
        print(response.url)

    #def parse(self, response):
     #   print('hola')
        # for title in response.css('.oxy-post-title'):
        #     yield {'title': title.css('::text').get()}

        # for next_page in response.css('a.next'):
        #     yield response.follow(next_page, self.parse)



if __name__=="__main__":
    process = CrawlerProcess({'USER_AGENT': 'AdsBot-Google'})
    date=dt(2021,3,30)
    process.crawl(scrapySkyscanner,origin='Madrid',destination='Barcelona',date=date)
    process.start()
    print("eoo")