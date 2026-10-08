import socket
HOST='0.0.0.0'
PORT=5001

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    while True:
        data, addr = s.recvfrom(4096)
        print(f"{addr}: {data.decode()}")
        respuesta = "Hola clientini"
        s.sendto(respuesta.encode(), addr)
