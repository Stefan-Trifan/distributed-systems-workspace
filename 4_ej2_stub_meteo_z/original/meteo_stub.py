import socket,json
class MeteoStub:
    def __init__(self,host,port): self.host,self.port=host,port
    def _request(self,op,ciudad):
        # TODO: ocultar comunicación aquí
        raise NotImplementedError
    def temperatura(self,ciudad): raise NotImplementedError
    def humedad(self,ciudad): raise NotImplementedError
    def pronostico(self,ciudad): raise NotImplementedError
