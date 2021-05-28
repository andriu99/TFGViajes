from .funtionsRequest.airportsRequests import getFlightInformation,getSessionKey,getTokenOrFlightData,getAirportsData
from .funtionsRequest.blablacarRequests import findBlablaTrips
from .funtionsRequest.bustrainRequests import findbustrainTrips
from .funtionsRequest.googleMapsRequests import getProvinceLocationThroughCoordinates,getTimeZone
from django.db import models
import requests 
import json 

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
    headers=models.JSONField(null=True,blank=True)

    RApi = models.ForeignKey(RESTApi, on_delete=models.CASCADE,related_name='requests')

    def __str__(self):
        return self.name
    
    
    def getResponse(self,baseUrl,listParamsValues,typeOfData=""):
        structureWithValues=dict(self.ParamsOrDataDictStructure)
        contIndex=0
        for key in structureWithValues.keys():
            structureWithValues[key]=listParamsValues[contIndex]
            contIndex+=1



        if self.typeRequests=="GET":
            return requests.get(baseUrl+self.PartToaddToBaseUrl,params=structureWithValues)
        else:
            if typeOfData=='str':
                structureWithValues=json.dumps(structureWithValues)

            rq=requests.post(baseUrl+self.PartToaddToBaseUrl,data=structureWithValues,headers=dict(self.headers))


            return rq


    def executeFunction(self,listParamsValues,typeOfData=""):
        baseUrl=self.RApi.BaseUrl
        response=self.getResponse(baseUrl,listParamsValues,typeOfData)
        functionName=self.funcToExtractDataFromJsonName
        return globals()[functionName](response)

    


class Node(models.Model):
    code=models.CharField(unique=True,max_length=10)
    name=models.CharField(max_length=70)
    latitude=models.FloatField()
    longitude=models.FloatField()
    location=models.CharField(max_length=50,default='Unknown')
    province=models.CharField(max_length=50,default='Unknown')

    class Suit(models.TextChoices):
        STATION = 'S'
        AIRPORT = 'A'
     

    nodeType = models.CharField(choices=Suit.choices,max_length=5)

    def __str__(self):
        return self.name+' ('+self.nodeType+')'

class Trip(models.Model):
    departureDate=models.DateTimeField()
    arrivalDate=models.DateTimeField()
    duration=models.IntegerField() #in seconds
    price=models.FloatField()

    departureNode=models.ForeignKey(Node,on_delete=models.CASCADE,related_name='departureNode',null=True)
    arrivalNode=models.ForeignKey(Node,on_delete=models.CASCADE,related_name='arrivalNode',null=True)


class blablaTrip(models.Model):
    trip=models.OneToOneField(Trip,on_delete=models.CASCADE,related_name='blablaTrip')
    link=models.URLField(max_length=150)
    departureCity=models.CharField(max_length=30)
    departureAddress=models.CharField(max_length=30)
    departureLatitude=models.FloatField()
    departureLongitude=models.FloatField()

    arrivalCity=models.CharField(max_length=30)
    arrivalAddress=models.CharField(max_length=30)
    arrivalLatitude=models.FloatField()
    arrivalLongitude=models.FloatField()

    # class Meta:
    #     unique_together = ('link', 'departureCity','departureAddress','departureLatitude','departureLongitude','arrivalLatitude','arrivalLongitude')



class skyscannerTrip(models.Model):
    trip=models.OneToOneField(Trip,on_delete=models.CASCADE,related_name='skyscannerTrip')
    urlPay=models.URLField(max_length=1500)
    airlineName=models.CharField(max_length=50)
    airlineUrlImage=models.CharField(max_length=50)

    
  
class busOrTrainTrip(models.Model):
    trip=models.OneToOneField(Trip,on_delete=models.CASCADE,related_name='busOrTrainTrip')

    class Suit(models.TextChoices):
        TRAIN = 'T'
        BUS = 'B'
     

    system = models.CharField(choices=Suit.choices,max_length=5)





    
        


