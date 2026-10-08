import socket
import time
import json

HOST = '127.0.0.1'
PORT=5001

def enviar(texto, c) :
    c.sendall(texto.encode())
    data = c.recv(4096)
    return data.decode()

with socket.create_connection((HOST, PORT), timeout=3) as c:
    c.settimeout(3)

    while True:
        time.sleep(2)

        # Ejemplo 2
        mensaje = {
            "type": "message",
            "text": "Hola servidor"
        }
        respuesta=enviar(json.dumps(mensaje), c)
        print(respuesta)

        mensaje = {
            "type": "time",
            "text": "Hola"
        }
        respuesta=enviar(json.dumps(mensaje), c)
        print(respuesta)
