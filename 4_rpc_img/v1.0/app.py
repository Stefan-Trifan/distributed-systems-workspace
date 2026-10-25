from rpc_client import RPCClient, RPCError

rpc = RPCClient('127.0.0.1',5003)

try:
    print(rpc.call('info_imagen', 'pepito.jpg'))
    print(rpc.call('escala_grises', 'pepito.jpg'))
    print(rpc.call('redimensionar', 'pepito.jpg', 800, 600))
except RPCError as e:
    print("Error capturado: ", e)

# probar procedimiento inexistente y argumentos incorrectos