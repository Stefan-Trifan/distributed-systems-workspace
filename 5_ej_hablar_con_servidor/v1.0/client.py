import socket
import json
import threading

HOST = '127.0.0.1'
PORT = 5001

def enviar():
    while True:
        print("broadcast \n-> ")
        mensaje = {
            'action': 'broadcast',
            'name': 'steve',
            'text': input()
        }
        # enviar
        c.sendall(json.dumps(mensaje).encode())

def recibir():
    while True:
        respuesta = c.recv(4096).decode()
        print("Respuesta:", respuesta)

# Conectar
with socket.create_connection((HOST, PORT), timeout = 30) as c:
    c.settimeout(30)

    mensaje = {
        'action': 'mynameis',
        'name': 'steve',
    }
    c.sendall(json.dumps(mensaje).encode())

    hilo_recibir = threading.Thread(
        target=recibir,
        args=(),
        daemon=True
    )
    hilo_recibir.start()

    enviar()