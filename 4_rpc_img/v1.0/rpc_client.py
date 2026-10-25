import socket,json

class RPCError(Exception):
    pass

class RPCClient:
    def __init__(self, host,port ,timeout = 3):
        self.host = host
        self.port = port
        self.timeout= timeout

    def call(self, function, *args):
        # done TODO: petición genérica, socket, JSON, respuesta y errores
        # Primera peticion
        peticion = {
            'function': function,
            'args': list(args)
        }

        try:
            with socket.create_connection((self.host, self.port), timeout = self.timeout) as c:
                c.settimeout(self.timeout)

                c.sendall(json.dumps(peticion).encode())

                respuesta = json.loads(c.recv(4096).decode())
        except OSError as e:
            raise RPCError("Problema del sistema operativo")

        if respuesta.get('status') == 'ok':
            return respuesta.get('result')
        else:
            raise RPCError("Error desde el otro lado")