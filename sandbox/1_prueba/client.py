import socket

HOST = '127.0.0.1'
PORT = 5001

with socket.create_connection((HOST, PORT), timeout=3) as c:
    c.settimeout(3)

    mensaje = "Hola servidor"

    c.sendall(mensaje.encode())

    data = c.recv(4096)
    respuesta = data.decode()

    print("Respuesta:", respuesta)