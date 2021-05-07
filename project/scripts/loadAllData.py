from .loadRequestsInfo import run as runRequest
from .loadAirportsData import run as runAirportsData
from .loadStationsData import run as runStationsData

def run():
    #runRequest()
    runAirportsData()
    runStationsData()