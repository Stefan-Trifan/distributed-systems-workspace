class RPCServer:
    def __init__(self): self.procedures={}
    def register(self,name,function):
        # TODO
        raise NotImplementedError
    def dispatch(self,request):
        # TODO: buscar función, ejecutar *args y gestionar errores
        raise NotImplementedError
