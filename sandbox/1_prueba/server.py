import socket

HOST = '0.0.0.0'
PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((HOST, PORT))
    s.listen()

    while True:
        c, address = s.accept()

        # atenderCliente()
        with c:
            while True:
                data = c.recv(4096)

                if not data:
                    break

                mensaje = data.decode()
                print(f"Recibido de {address}: {mensaje}")

                respuesta = "Hola cliente"
                c.sendall(respuesta.encode())