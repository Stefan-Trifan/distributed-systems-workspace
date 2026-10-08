import socket
import time

HOST = '127.0.0.1'
PORT=5001

def enviar(texto, c):
    # manda los bytes decodificados
    # por la conexión TCP.
    c.sendall(texto.encode()) # Marshall

    # Dame datos que hayan llegado por esta conexión TCP
    data = c.recv(4096)

    return data.decode() # Unmarshall

# Conceptualmente parecido a:
# - socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# - s.connect((HOST, PORT))
# timeout: intento inicial de establecer la conexión
with socket.create_connection((HOST, PORT), timeout=3) as c:

    # settimeout: configura el socket para que
    # las operaciones posteriores que bloqueen (ej: c.recv(...))
    # no esperen indefinidamente.
    c.settimeout(3)

    while True:
        time.sleep(2)

        # Ejemplo 1
        mensaje = "Hola servidor"
        respuesta = enviar(mensaje, c)
        print(respuesta)
