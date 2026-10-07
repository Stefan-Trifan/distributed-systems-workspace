import socket
import json

HOST, PORT = '127.0.0.1', 5002


# Funciones que deben implementar los alumnos
def temperatura(ciudad):
    if ciudad=='Madrid':
        return 21
    return None

def humedad(ciudad):
    if ciudad=='Madrid':
        return 10
    return None

def pronostico(ciudad):
    if ciudad=='Madrid':
        return "Maremoto"
    return None


def procesar(r):
    ciudad = r.get('ciudad')
    operacion = r.get('operacion')

    if operacion == 'temperatura':
        resultado = temperatura(ciudad)

    elif operacion == 'humedad':
        resultado = humedad(ciudad)

    elif operacion == 'pronostico':
        resultado = pronostico(ciudad)

    else:
        return {
            'status': 'error',
            'message': 'Operacion desconocida'
        }

    if resultado is None:
        return {
            'status': 'error',
            'message': 'Ciudad no disponible'
        }

    return {
        'status': 'ok',
        'result': resultado
    }


with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()

    while True:
        c, _ = s.accept()

        with c:
            r = json.loads(c.recv(4096).decode())
            respuesta = procesar(r)
            c.sendall(json.dumps(respuesta).encode())