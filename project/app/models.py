from django.db import models
import requests as rq


#help: https://stackoverflow.com/questions/58558989/what-does-djangos-property-do
class request(models.Model):
    
    description=models.CharField(max_length=200)
    PartToaddToBaseUrl=models.CharField(max_length=200)
    funcToExtractDataFromJsonName=models.CharField(max_length=100)
    ParamsOrDataDictStructure=models.JSONField()

    class Suit(models.TextChoices):
        GET = 'GET'
        POST = 'POST'
     

    typeRequests = models.CharField(choices=Suit.choices)

    

    @property
    def getJson(self,baseUrl,listParamsValues):
        structureWithValues=dict(self.ParamsOrDataDictStructure)
        contIndex=0
        for key in structureWithValues.keys():
            structureWithValues[key]=listParamsValues[contIndex]
            contIndex+=1
        if typeRequests=="GET":
        else:
            
        
    
    @property
    def executeFunction(self,listParamsValues):
        return exec(self.funcToExtractDataFromJsonName+'('+'self.fillParamsOrDataDictStructure'+'('+'listParamsValues'+')'+')')
        


