import socket,json
class MeteoStub:
    def __init__(self,host,port): self.host,self.port=host,port
    def _request(self,op,ciudad):
        with socket.create_connection((self.host, self.port), timeout=3) as c:
            request=json.dumps({'operacion': op, 'ciudad':ciudad})
            c.sendall(request.encode())
            answer=c.recv(4096).decode()
            r=json.loads(answer)
        if r.get('status')!='ok':
            raise RuntimeError(r.get('message'))
        return r['result']

    def temperatura(self,ciudad):
        return self._request('temperatura', ciudad)
    def humedad(self,ciudad):
        return self._request('humedad', ciudad)
    def pronostico(self,ciudad):
        return self._request('pronostico', ciudad)
