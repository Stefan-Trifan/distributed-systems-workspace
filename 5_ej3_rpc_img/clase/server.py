import socket,json
from concurrent.futures import ThreadPoolExecutor
from rpc_server import RPCServer
from procedures import info_imagen,escala_grises,redimensionar

HOST,PORT='127.0.0.1',5003

rpc = RPCServer()
rpc.register("info_imagen", info_imagen)
rpc.register("escala_grises", escala_grises)
rpc.register("redimensionar", redimensionar)

# done TODO: registrar procedimientos
def atender(c,a):
    # done TODO: recibir, dispatch, responder
    print("ATENDIENDO PETICION")
    msgin = c.recv(4096).decode()

    try:
        resp = rpc.dispatch(json.loads(msgin))
    except Exception as e:
        resp = {"status":"Error", "error":"BAD_MESSAGE", "message":str(e)}

    stringRespuesta = json.dumps(resp)
    c.sendall(stringRespuesta.encode())

with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1); s.bind((HOST,PORT)); s.listen()

    # done TODO: usar ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=3) as pool:

        while True:
            c,a=s.accept()
            # atender(c,a)
            pool.submit(atender, c, a)
