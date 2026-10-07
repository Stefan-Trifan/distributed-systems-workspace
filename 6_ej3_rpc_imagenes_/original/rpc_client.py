import socket,json
class RPCError(Exception): pass
class RPCClient:
    def __init__(self,host,port,timeout=3): self.host,self.port,self.timeout=host,port,timeout
    def call(self,function,*args):
        # TODO: petición genérica, socket, JSON, respuesta y errores
        raise NotImplementedError
