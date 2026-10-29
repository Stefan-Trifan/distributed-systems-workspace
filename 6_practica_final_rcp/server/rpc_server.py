# Esqueleto del servidor RPC.

# El alumno debe completar el registro, dispatch, gestión de errores
# y posteriormente la concurrencia.

from __future__ import annotations

from typing import Any, Callable

class RPCServer:
    def __init__(self):
        # DONE (alumno):
        # Crear una estructura para registrar procedimientos.
        self._procedures: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, function: Callable[..., Any]) -> None:
        # Registra un procedimiento remoto.
        # # DONE (alumno):
        # Implementar el registro.

        if not callable(function):
            raise TypeError("No callable function")
        self._procedures[name] = function


    def dispatch(self, request: dict[str, Any]) -> dict[str, Any]:
        # done (alumno):
        # Procesa una petición RPC y construye la respuesta.
        # Formato de entrada esperado:
        # {
        #     "function": "sumar",
        #     "args": [4, 7]
        # }
        name = request.get("function")
        args = request.get("args", [])

        # done Validar el formato de la petición.
        # Comprobamos que name es un string
        if not isinstance(name, str):
            return {
                "status": "error",
                "error": "INVALID_FUNCTION",
                "message": "El nombre de la funcion tiene formato incorrecto",
            }

        # done - Gestionar argumentos incorrectos.
        if not isinstance(args, list):
            return {
                "status": "error",
                "error": "INVALID_ARGS",
                "message": "El formato de los argumentos es invalido",
            }

        # done - Gestionar procedimiento inexistente.
        if name not in self._procedures:
            return {
                "status": "error",
                "error": "PROCEDURE_NOT_FOUND",
                "message": "La funcion no ha sido registrada",
            }

        try:
            # done - Buscar el procedimiento.
            # done - Ejecutarlo.
            # done - Construir respuesta status = ok.
            thisResult = self._procedures[name](*args)
            return {
                "status":"ok",
                "result": thisResult
            }
        except Exception as e:
             # done - Gestionar excepciones de ejecución.
            return {
                "status":"error",
                "error":"EXECUTION_ERROR",
                "message": str(e)
            }




