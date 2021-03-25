class NotFoundTrip(Exception):
    def __init__(self,origin,destination,MeanOfTransport,mensaje=None):
        self.mensaje='No se encontraron viajes entre {origin} y {destino} en {MeanOfTransport}'


