import socket

HOST = '0.0.0.0'
PORT = 5001

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

            # Ejemplo 1
            respuesta="Hola cliente"
            c.sendall(respuesta.encode())


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

    # Después de terminar con un cliente, vuelve a esperar a otro.
    while True:
        # accept() se dedica a recibir conexiones
        # c -> SOCKET DE COMUNICACIÓN
        # el socket de la conexión TCP
        # establecida con ese cliente.
        c, addr = s.accept()

        print(f"Recibida conexion de {addr}")
        atender_cliente(c, addr)