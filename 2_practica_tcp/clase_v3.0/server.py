import socket
import json
from datetime import datetime
import threading

HOST = '0.0.0.0'
PORT = 5001

def procesar(r):
    if r.get('type') == 'message':
        respuesta={
            'status':'ok',
            'message': 'Hola cliente'
        }
        return respuesta

    if r.get('type')=='time':
        respuesta={
            'status': 'ok',
            'time': datetime.now().strftime('%H:%M:%S')
        }
        return respuesta

    return{'status':'error', 'message':'Orden desconocida'}

def atender_cliente(c, addr):
    with c:
        while True:
            data = c.recv(4096)

            if not data:
                break
            
            print(f"Recibido de {addr}: {data.decode()}")

            # Ejemplo 2
            respuesta=procesar(json.loads(data.decode()))
            c.sendall(json.dumps(respuesta).encode())


# Creamos un socket de tipo internet para TCP. De tipo stream
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()

    while True:
        c, addr = s.accept() # c= conexion
        print(f"Recibida conexion de {addr}")
        # atender_cliente(c, addr)
        hilo = threading.Thread(
            target = atender_cliente,
            args = (c,addr),
            daemon = True
        )

        hilo.start()