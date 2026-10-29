"""Esqueleto de la capa cliente RPC.

Esta clase debe ocultar a la aplicación:
- creación del mensaje
- serialización
- conexión TCP
- envío y recepción
- tratamiento de errores
"""

from __future__ import annotations

import socket
from typing import Any

from common.protocol import send_json, recv_json

class RPCClient:
    def __init__(self, host: str, port: int, timeout: float = 5.0):
        self.host = host
        self.port = port
        self.timeout = timeout

    def call(self, function: str, *args: Any) -> Any:
        # Ejecuta un procedimiento remoto y devuelve su resultado.

        # done 1. Crear la petición RPC.
        peticion = {
            'function': function,
            'args': list(args)
        }

        try:
            # done 2. Abrir una conexión TCP.
            # done 3. Configurar timeout.
            with socket.create_connection((self.host, self.port), timeout = self.timeout) as c:
                c.settimeout(self.timeout)
                # done 4. Enviar la petición.
                send_json(c, peticion)

                # done 5. Recibir la respuesta.
                respuesta = recv_json(c)

        # done 8. Gestionar fallos de comunicación sin bloquear indefinidamente.
        except socket.timeout:
            raise RuntimeError("TIMEOUT. El servidor no ha respondido a tiempo")

        except OSError as e:
            raise RuntimeError(f"COMMUNICATION_ERROR: {e}")

        # done 6. Devolver el resultado si status == "ok".
        if respuesta.get("status") == "ok":
            return respuesta.get("result")

        # done 7. Gestionar respuestas de error.
        else:
            error = respuesta.get("error", "UNKNOWN_ERROR")
            message = respuesta.get("message", "")
            raise RuntimeError(f"{error}: {message}")