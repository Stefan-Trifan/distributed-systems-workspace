import socket
import json
from datetime import datetime
import threading

HOST = '0.0.0.0'
PORT = 5001

def procesar(r):
    if r.get('type') == 'message':
        respuesta = {
            'status':'ok',
            'message': 'Hola cliente'
        }
        return respuesta

    if r.get('type') =='time':
        respuesta = {
            'status': 'ok',
            'time': datetime.now().strftime('%H:%M:%S')
        }
        return respuesta

    return{
        'status':'error',
        'message':'Orden desconocida'
    }

def atender_cliente(c, addr):
    # with simplemente gestiona el socket
    # se encargará de cerrarlo cuando salgamos del bloque
    with c:

        # Mientras este cliente siga conectado,
        # sigue recibiendo mensajes de él
        while True:

            # Espera: datos de la conexión que ya existe
            data = c.recv(4096)

            if not data:
                break

            print(f"Recibido de {addr}: {data.decode()}")

            # Ejemplo 2
            # loads: convierte JSON -> diccionario
            respuesta = procesar(json.loads(data.decode()))
            # dumps: convierte diccionario -> JSON.
            c.sendall(json.dumps(respuesta).encode())


# Creamos un socket
# s -> SOCKET DE ESCUCHA
# AF_INET: Utiliza IPv4
# SOCK_STREAM: TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # No importa. Configura una opción del socket
    # Permite reutilizar la dirección local en determinadas situaciones,
    # útil cuando reinicias rápidamente el servidor
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Asocia este socket con esta dirección y este puerto
    s.bind((HOST, PORT))

    # Este socket va a actuar como socket servidor
    # y está preparado para aceptar conexiones entrantes.
    s.listen()

    # Estamos esperando una conexión TCP.

    while True:
        # accept() se dedica a recibir conexiones
        # c -> SOCKET DE COMUNICACIÓN
        # el socket de la conexión TCP
        # establecida con ese cliente.
        c, addr = s.accept() # c= conexion
        print(f"Recibida conexion de {addr}")

        # Crea un objeto hilo cuya función de trabajo será atender_cliente
        # pásale como argumentos c y addr
        # configúralo como daemon
        hilo = threading.Thread(
            target = atender_cliente,
            args = (c,addr),
            daemon = True
        )

        # Inicia este hilo
        hilo.start()