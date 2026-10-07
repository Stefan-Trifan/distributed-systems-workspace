# Servidor UDP para la clase mejor del mundo
import socket

# Variables
# Que escuche mensajes de todas las ip que van al puerto 5001
HOST='0.0.0.0'
PORT=5001

# Constructor crea socket que será llamado s

# AF_INET quiero que el socket sea del tipo internet,
# protocolo IP
# SOCK_DGRAM quiero que reciba mensajes UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))

    while True:
        # Con recvfrom nos permite recibir los mensajes
        # y el numero es el tam max de bytes del mensaje
        data, adress = s.recvfrom(4096)
        # Data son datos en puros bytes asi que tengo
        # qu convertirlo al formato legible (Unmarshall)
        print(f"Recibido de {adress}: {data.decode()}")

        respuesta="Mensaje recibido"
        # respondo al cliente mandondole un mensaje
        # codificado al que me habia enviado el mensaje.
        s.sendto(respuesta.encode(), adress)








