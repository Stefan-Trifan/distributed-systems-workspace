import socket

# Variables
# Host con el que nos queremos conectar, este caso nosotros mismos localhost
HOST='127.0.0.1'
PORT=5001

def enviar(texto):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(3)
        # Vamos a convertir el mensaje a bytes
        s.sendto(texto.encode(), (HOST, PORT))
        # Recibimos la respuesta del server
        data, adress = s.recvfrom(4096)
        print("Respuesta:", data.decode())

enviar("Hola mundo")
