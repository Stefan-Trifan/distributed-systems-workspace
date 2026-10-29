"""Cliente de ejemplo proporcionado.

Primero demuestra paso de mensajes explícito.
Cuando RPCClient esté implementado, el alumno puede sustituir esta
parte por llamadas `rpc.call(...)`.
"""

from __future__ import annotations
import socket
from common.protocol import send_json, recv_json
from client.rpc_client import RPCClient

# done Sustituir por IP/DNS de EC2 al desplegar
HOST = "34.239.59.61"
PORT = 5001

def main():

    # Cuando RPCClient esté completo:
    rpc = RPCClient(HOST, PORT)
    print("sumar:", rpc.call("sumar", 4, 7))
    print("multiplicar:", rpc.call("multiplicar", 3, 5))
    print("potencia:", rpc.call("potencia", 2, 4))

    print("validar IPv4 correcta:", rpc.call("validar_ipv4", "192.168.1.10"))
    print("validar IPv4 incorrecta:", rpc.call("validar_ipv4", "192.168.300.10"))

    print("factorial_recursivo:", rpc.call("factorial_recursivo", 5))

    print(rpc.call("tarea_lenta", 3))

if __name__ == "__main__":
    main()
