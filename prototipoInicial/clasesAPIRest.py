from datetime import datetime as dt
from datetime import timedelta
import json
import requests as rq

class requests:
    '''
    PartToaddToBaseUrl: String to add to base url 
    ParamsOrDataDictStructure: Estructura del diccionario con la información a enviar (diccionario con valores como cadena vacía)
    funcToExtractDataFromJson: Función para devolver los datos dado el json
    '''
    def __init__(self,id,description,PartToaddToBaseUrl,ParamsOrDataDictStructure,funcToExtractDataFromJson):
        self.id=id
        self.description=description
        self.PartToaddToBaseUrl=PartToaddToBaseUrl
        self.ParamsOrDataDictStructure=ParamsOrDataDictStructure
        self.funcToExtractDataFromJson=funcToExtractDataFromJson

    def getId(self):
        return self.id

    def getdescription(self):
        return self.description
    '''
    Partimos del dicccionario con las claves pero sin valores. Lo rellenamos
    listParamsValues:Valores para las claves del diccionario que enviaremos vía GET o POST.
    return: Diccionario con los valores para hacer la petición HTTP
    '''
    def getParamsOrDataDict(self,listParamsValues):
        structureWithValues=self.ParamsOrDataDictStructure
        contIndex=0
        for key in structureWithValues.keys():
            structureWithValues[key]=listParamsValues[contIndex]
            contIndex+=1
        return structureWithValues

    def setDescription(self,description):
        self.description=description

    def setId(self,id):
        self.id=id

    def setParamOrDataStructure(self,ParamsOrDataDictStructure):
        self.ParamsOrDataDictStructure=ParamsOrDataDictStructure

    def setPartToaddToBaseUrl(self,PartToaddToBaseUrl):
        self.PartToaddToBaseUrl=PartToaddToBaseUrl

    def setfuncToExtractDataFromJson(self,func):
        self.funcToExtractDataFromJson=func

    def extractDataFromJson(self,json):
        return self.funcToExtractDataFromJson(json)

    


class getRequests(requests):
    idGetNumber=1
    '''
    PartToaddToBaseUrl: String to add to base url 
    ParamsOrDataDictStructure: Estructura del diccionario con la información a enviar
    '''
    def __init__(self,description,PartToaddToBaseUrl,ParamsOrDataDictStructure,funcToExtractDataFromJson):
        id="GET"+str(self.idGetNumber)
        self.idGetNumber=self.idGetNumber+1
        super().__init__(id,description,PartToaddToBaseUrl,ParamsOrDataDictStructure,funcToExtractDataFromJson)
    
    def execute(self,baseUrl,listValues):
        paramsDict=super().getParamsOrDataDict(listValues)
        return rq.get(baseUrl+self.PartToaddToBaseUrl,params=paramsDict)

    



class postRequests(requests):
    idPostNumber=1
    '''
    PartToaddToBaseUrl: String to add to base url 
    ParamsOrDataDictStructure: Estructura del diccionario con la información a enviar
    '''
    def __init__(self,description,PartToaddToBaseUrl,headers,ParamsOrDataDictStructure,funcToExtractDataFromJson):
        id="POST"+str(self.idPostNumber)
        self.idPostNumber=self.idPostNumber+1
        super().__init__(id,description,PartToaddToBaseUrl,ParamsOrDataDictStructure,funcToExtractDataFromJson)
        self.headers=headers
    
    def getHeaders(self):
        return self.headers

    def setHeaders(self,headers):
        self.headers=headers

    def execute(self,baseUrl,typeOfData,listValues):
        data=super().getParamsOrDataDict(listValues)
        if typeOfData=='str':
            data=json.dumps(data)

        return rq.post(baseUrl+self.PartToaddToBaseUrl,headers=self.headers,data=data)
    


    
class RESTApi:
    def __init__(self,BaseUrl,APIKey,requests=[]):
        self.BaseUrl=BaseUrl
        self.APIKey=APIKey
        self.requests=requests
    
    def getBaseUrl(self):
        return self.BaseUrl

    def getAPIKey(self):
        return self.APIKey
    
    def getRequests(self):
        return self.requests

    def setBaseUrl(self,BaseUrl):
        self.BaseUrl=BaseUrl

    def setAPIKey(self,APIKey):
        self.APIKey=APIKey

    def setRequests(self,requests):
        self.requests=requests

    def addRequests(self,request):
        self.requests.append(request)


# paramsStructure={'key':'','from_coordinate':'','to_coordinate':'','currency':'','start_date_local':'','end_date_local':''}
# fecha=dt(2021,4,25)
# listParamsValues=['','40.416775,-3.703791','41.3887900,2.1589900','EUR',fecha.isoformat(),(fecha+timedelta(days=1)).isoformat()]

# def ProcesaJsonBlablaCar(response_json):
#     for trip in response_json['trips']:
#             originData=trip['waypoints'][0]
#             destinationData=trip['waypoints'][1]
#             yield (
#                     trip['link'],
#                     originData['date_time'],
#                     destinationData['date_time'],
#                     originData['place']['address'],
#                     destinationData['place']['address'],
#                     originData['place']['latitude'],
#                     originData['place']['longitude'],
#                     destinationData['place']['latitude'],
#                     destinationData['place']['longitude'],
#                     trip['price']['amount']
#                    )
    
# getRequestsBlabla=getRequests('Get information about blablacar´s trips', '/api/v3/trips', paramsStructure,ProcesaJsonBlablaCar)
# BlablaCarRESTApi=RESTApi('https://public-api.blablacar.com','UIbM2vkhEdrrTLiLnrQkBqgPxrv7S4mI')
# BlablaCarRESTApi.addRequests(getRequestsBlabla)
# listParamsValues[0]=BlablaCarRESTApi.getAPIKey()
# response=BlablaCarRESTApi.requests[0].execute(BlablaCarRESTApi.getBaseUrl(),listParamsValues)

# for (link,tStart,tEnd,
#     addressStart,addressEnd,latStart,
#     lonStart,latEnd,longStart,price) in getRequestsBlabla.extractDataFromJson(response.json()):

#     print(addressStart)
    


