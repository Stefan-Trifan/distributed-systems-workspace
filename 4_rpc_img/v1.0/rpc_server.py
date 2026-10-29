class RPCServer:
    def __init__(self):
        self.procedures = {}

    def register(self, name, function):
        if not callable(function):
            raise TypeError("No callable function")

        self.procedures[name] = function

    def dispatch(self, request):
        # done TODO: buscar función, ejecutar *args y gestionar errores
        name = request.get("function")
        args = request.get("args", [])
        if name not in self.procedures:
            raise TypeError("ERROR. Nombre de funcion no existente")

        try:
            thisResult = self.procedures[name](*args)
            return {
                "status":"ok",
                "result": thisResult
            }
        except Exception as e:
            return {
                "status":"error",
                "error":"EXECUTION_ERROR",
                "message": str(e)
            }
