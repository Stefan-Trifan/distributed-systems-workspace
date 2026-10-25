# Práctica 1: comunicación con UDP

En esta práctica estamos aprendiendo a enviar y recibir mensajes entre un cliente y un servidor usando sockets UDP en Python.

- `server.py`: espera mensajes en el puerto `5001`, los muestra por pantalla y responde con «Hola clientini». Sigue esperando nuevos mensajes hasta que lo paramos.
- `client.py`: envía «Hola servidorino» al servidor en `127.0.0.1` (nuestro propio ordenador) y muestra la respuesta. Espera un máximo de 3 segundos.

Los mensajes se convierten a bytes con `encode()` para enviarlos y se vuelven a convertir a texto con `decode()` al recibirlos. UDP permite enviar mensajes sin establecer antes una conexión, pero no garantiza que lleguen.

## Cómo ejecutarlo

Necesitamos Python 3. No hace falta instalar librerías adicionales.

Desde este directorio, abrimos una terminal y arrancamos el servidor:

```bash
python3 server.py
```

En otra terminal, también desde este directorio, ejecutamos el cliente:

```bash
python3 client.py
```

El cliente mostrará `Respuesta: Hola clientini` y terminará. Para parar el servidor, pulsamos `Ctrl+C` en su terminal.
