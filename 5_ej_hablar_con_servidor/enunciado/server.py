import socket
import json
import threading


HOST, PORT = '0.0.0.0', 5001

# Diccionario: socket -> nombre del cliente
# El nombre será None mientras el cliente no se identifique.
clientes = {}


def atender_cliente(c, addr):
    # Registramos la nueva conexión
    clientes[c] = None

    with c:
        while True:
            data = c.recv(4096)

            print("Recibido:", data.decode())

            # El cliente ha cerrado la conexión
            if not data:
                break

            try:
                mensaje = json.loads(data.decode())
            except json.JSONDecodeError:
                print(f"JSON incorrecto recibido de {addr}")
                continue

            action = mensaje.get("action")

            # action es obligatorio
            if action is None:
                print(f"Mensaje sin action recibido de {addr}")
                continue

            # Enviar el mensaje a todos los clientes conectados
            # COMENZAR POR USAR SOLO ESTA ACCION
            if action == "broadcast":
                for otro_socket in clientes:
                    otro_socket.sendall(data)

            # Asociar un nombre a esta conexión
            elif action == "mynameis":
                name = mensaje.get("name")

                if name is not None:
                    clientes[c] = name
                    print(f"{addr} se identifica como {name}")

            # Enviar un mensaje a un cliente concreto
            elif action == "messageto":
                name = mensaje.get("name")

                for otro_socket, otro_nombre in clientes.items():
                    if otro_nombre == name:
                        otro_socket.sendall(data)
                        break

            else:
                print(f"Acción desconocida: {action}")

    # Eliminamos la conexión cuando el cliente se desconecta
    del clientes[c]
    print(f"Cliente {addr} desconectado")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((HOST, PORT))
    s.listen()

    print(f"Servidor escuchando en el puerto {PORT}")

    while True:
        c, addr = s.accept()
        print(f"Nueva conexión de {addr}")

        hilo = threading.Thread(
            target=atender_cliente,
            args=(c, addr),
            daemon=True
        )
        hilo.start()