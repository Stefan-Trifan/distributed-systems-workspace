# Servidor UDP para la clase mejor del mundo
import socket

# Escucha mensajes de todas las ip que van al puerto 5001
HOST='0.0.0.0'
PORT=5001

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))

    while True:
        # recvfrom permite recibir mensajes
        # 4096 es el tam max de bytes del mensaje
        data, adress = s.recvfrom(4096)

        # Data son datos en puros bytes asi que tengo
        # que convertirlo al formato legible (Unmarshall)
        print(f"- {adress}: {data.decode()}")

        # respondo al cliente mandondole un mensaje
        # codificado al que me habia enviado el mensaje.
        respuesta="Hola clientini"
        s.sendto(respuesta.encode(), adress)








