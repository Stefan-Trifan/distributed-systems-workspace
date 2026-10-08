import socket
HOST='127.0.0.1'
PORT=5001

def enviar(texto):
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
        s.settimeout(3)
        s.sendto(texto.encode(), (HOST, PORT))
        data, addr = s.recv(4096)
        print("Respuesta", data.decode())

enviar("Hola servidorino")