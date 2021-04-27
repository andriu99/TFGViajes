from django.db import models
import requests 
import json

#help: https://stackoverflow.com/questions/58558989/what-does-djangos-property-do
class request(models.Model):
    
    description=models.CharField(max_length=200)
    PartToaddToBaseUrl=models.CharField(max_length=200)
    funcToExtractDataFromJsonName=models.CharField(max_length=100)
    ParamsOrDataDictStructure=models.JSONField()
    headers=models.JSONField(null=True)

    class Suit(models.TextChoices):
        GET = 'GET'
        POST = 'POST'
     

    typeRequests = models.CharField(choices=Suit.choices,max_length=5)

    @property
    def getJson(self,baseUrl,listParamsValues,typeOfData=""):
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

            return requests.post(baseUrl+self.PartToaddToBaseUrl,data=structureWithValues,headers=dict(self.headers))


    @property
    def executeFunction(self):
        json=self.getJson()
        return exec(self.funcToExtractDataFromJsonName+'(json)')


class RESTApi(models.Model):
    BaseUrl=models.CharField(max_length=50)
    APIKey=models.CharField(max_length=50)
    Requests = models.ForeignKey(request, on_delete=models.CASCADE)
    
  




    
        


