"""Esqueleto del servidor RPC.

El alumno debe completar el registro, dispatch, gestión de errores
y posteriormente la concurrencia.
"""

from __future__ import annotations

from typing import Any, Callable

class RPCServer:
    def __init__(self):
        # TODO (alumno):
        # Crear una estructura para registrar procedimientos.
        self._procedures: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, function: Callable[..., Any]) -> None:
        """Registra un procedimiento remoto.

        TODO (alumno):
        Implementar el registro.
        """
        raise NotImplementedError("Completar RPCServer.register()")

    def dispatch(self, request: dict[str, Any]) -> dict[str, Any]:
        """Procesa una petición RPC y construye la respuesta.

        Formato de entrada esperado:
        {
            "function": "sumar",
            "args": [4, 7]
        }

        TODO (alumno):
        - Validar el formato de la petición.
        - Buscar el procedimiento.
        - Ejecutarlo.
        - Construir respuesta status=ok.
        - Gestionar procedimiento inexistente.
        - Gestionar argumentos incorrectos.
        - Gestionar excepciones de ejecución.
        """
        raise NotImplementedError("Completar RPCServer.dispatch()")
