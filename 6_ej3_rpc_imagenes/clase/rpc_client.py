import socket,json

class RPCError(Exception):
    pass

class RPCClient:
    def _init_(self,host,port,timeout=3):
        self.host = host
        self.port = port
        self.timeout= timeout

    def call(self,function,*args):
        # TODO: petición genérica, socket, JSON, respuesta y errores
        #Primera peticion
        req={'funcion': function, 'args': list(args)} #objeto json

        try:
            with socket.create_connection((self.host, self.port), timeout=self.timeout) as c:
                #Establezco tiempo de espera
                c.settimeout(self.timeout)
                #Convierto en String y de string a byes
                c.sendall(json.dumps(req).encode)
                rbytes= c.recv(4096)
                #Cargo la respuesta en un json
                r = json.loads(rbytes.decode())
        except OSError as e:
            raise RPCError("Problema del sistema operativo")

        if r.get('status') == 'ok':
            return r.get('result')
        else:
            raise RPCError("Error desde el otro lado")