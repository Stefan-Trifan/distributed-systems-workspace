import socket

# Host al que nos queremos conectar
HOST='127.0.0.1' # localhost (nosotros)
PORT=5001


def enviar(texto):
    # Constructor crea socket llamado s
    # AF_INET: Direcciones ipv4
    # SOCK_DGRAM: UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # No esperes mas de 3 segundos
        s.settimeout(3)

        # Vamos a convertir el mensaje a bytes
        s.sendto(texto.encode(), (HOST, PORT))

        # Recibimos la respuesta del server
        data, adress = s.recvfrom(4096)
        print("Respuesta:", data.decode())

enviar("Hola servidorino")
