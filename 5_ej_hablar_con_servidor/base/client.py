import socket
import time

HOST = '100.51.193.112'
PORT=5001

def enviar(texto, c):
    c.sendall(texto.encode())

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
        mensaje = "Alfredo Maricon"
        enviar(mensaje, c)
        time.sleep(0.1)
