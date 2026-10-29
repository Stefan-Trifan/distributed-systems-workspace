"""Servidor TCP mínimo proporcionado.

Esta versión acepta una conexión cada vez y devuelve una respuesta
temporal. El alumno deberá integrar RPCServer y convertirlo después
en un servidor concurrente.
"""

from __future__ import annotations

import socket, threading

from common.protocol import send_json, recv_json
from server.rpc_server import RPCServer
from server.procedures import (
    sumar,
    multiplicar,
    potencia,
    tarea_lenta,
    factorial_recursivo,
    validar_ipv4
)

HOST = "0.0.0.0"
PORT = 5001

def atender_cliente(c, addr, rpc_server):
    with c:
        print(f"Conexión recibida desde {addr}")

        try:
            request = recv_json(c)
            print("Mensaje recibido:", request)

            # done TODO (alumno):
            # done todo Sustituir por:
            response = rpc_server.dispatch(request)
            send_json(c, response)

        except Exception as exc:
            print(f"Error atendiendo la conexión: {exc}")

def main():
    print(f"Servidor escuchando en {HOST}:{PORT}")

    rpc_server = RPCServer()
    rpc_server.register("sumar", sumar)
    rpc_server.register("multiplicar", multiplicar)
    rpc_server.register("potencia", potencia)
    rpc_server.register("tarea_lenta", tarea_lenta)
    rpc_server.register("factorial_recursivo", factorial_recursivo)
    rpc_server.register("validar_ipv4", validar_ipv4)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        while True:
            c, addr = s.accept()

            # DONE (alumno):
            # Esta implementación es secuencial.
            # Modificarla al final de la práctica para atender
            # múltiples clientes simultáneamente.
            thread = threading.Thread(
                target = atender_cliente,
                args = (c, addr, rpc_server)
            )

            thread.start()

if __name__ == "__main__":
    main()
