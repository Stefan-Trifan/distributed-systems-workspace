import socket,json
from concurrent.futures import ThreadPoolExecutor
from rpc_server import RPCServer
from procedures import info_imagen,escala_grises,redimensionar
HOST,PORT='127.0.0.1',5003
rpc=RPCServer()
# TODO: registrar procedimientos
def atender(c,a):
    # TODO: recibir, dispatch, responder
    pass
with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1); s.bind((HOST,PORT)); s.listen()
    # TODO: usar ThreadPoolExecutor
    while True:
        c,a=s.accept(); atender(c,a)
