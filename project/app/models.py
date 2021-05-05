from .funtionsRequest.airportsRequests import getAirportID,getFlightInformation,getSessionKey,getTokenOrFlightData
from .funtionsRequest.blablacarRequests import findBlablaTrips
from .funtionsRequest.bustrainRequests import findbustrainTrips

import json

from django.db import models
import requests 
from json import dumps
#help: https://stackoverflow.com/questions/58558989/what-does-djangos-property-do


class RESTApi(models.Model):
    name=models.CharField(unique=True,max_length=50)
    BaseUrl=models.CharField(max_length=50)
    APIKey=models.CharField(max_length=50)


    def __str__(self):
        return self.name



class Request(models.Model):
    name=models.CharField(unique=True,max_length=50)
    description=models.CharField(max_length=200)
    PartToaddToBaseUrl=models.CharField(max_length=200)
    funcToExtractDataFromJsonName=models.CharField(max_length=100)
    ParamsOrDataDictStructure=models.JSONField()
    
    class Suit(models.TextChoices):
        GET = 'GET'
        POST = 'POST'
     

    typeRequests = models.CharField(choices=Suit.choices,max_length=5)
    headers=models.JSONField(null=True)

    RApi = models.ForeignKey(RESTApi, on_delete=models.CASCADE,related_name='requests')

    def __str__(self):
        return self.name
    
    
    def getResponse(self,baseUrl,listParamsValues,typeOfData=""):
        structureWithValues=json.load(self.ParamsOrDataDictStructure)
        contIndex=0
        for key in structureWithValues.keys():
            structureWithValues[key]=listParamsValues[contIndex]
            contIndex+=1

        if self.typeRequests=="GET":
            return requests.get(baseUrl+self.PartToaddToBaseUrl,params=structureWithValues)
        else:
            if typeOfData=='str':
                structureWithValues=dumps(structureWithValues)

            return requests.post(baseUrl+self.PartToaddToBaseUrl,data=structureWithValues,headers=dict(self.headers))


    def executeFunction(self,baseUrl,listParamsValues,typeOfData=""):
        response=self.getResponse(baseUrl,listParamsValues,typeOfData)
        functionName=self.funcToExtractDataFromJsonName
        return globals()[functionName](response)

    
  
   



class Node(models.Model):
    code=models.CharField(max_length=10)
    name=models.CharField(max_length=70)
    latitude=models.CharField(max_length=30)
    longitude=models.CharField(max_length=30)
    class Suit(models.TextChoices):
        STATION = 'S'
        AIRPORT = 'A'
     

    nodeType = models.CharField(choices=Suit.choices,max_length=5)



    
  




    
        


