# Práctica 4: llamadas RPC de imágenes

En esta práctica estamos aprendiendo a crear un sistema RPC (llamada a un procedimiento remoto). La aplicación pide ejecutar una función en el servidor indicando su nombre y sus argumentos, y recibe el resultado.

Por ejemplo, con `rpc.call('redimensionar', 'pepito.jpg', 800, 600)` pedimos al servidor que ejecute `redimensionar('pepito.jpg', 800, 600)`. El cliente RPC oculta el envío y la recepción de mensajes por la red.

## Qué hace cada archivo

- `app.py`: hace tres llamadas de ejemplo y muestra sus resultados. También captura los errores de tipo `RPCError`.
- `rpc_client.py`: convierte el nombre de la función y sus argumentos en una petición JSON, la envía por TCP y devuelve el resultado o lanza un `RPCError`.
- `server.py`: escucha en `127.0.0.1:5003`, registra las funciones disponibles y recibe las peticiones. Usa `ThreadPoolExecutor` con 3 hilos para atender hasta tres peticiones a la vez.
- `rpc_server.py`: guarda las funciones registradas. Su método `dispatch()` busca la función solicitada, la ejecuta con los argumentos recibidos y prepara la respuesta.
- `procedures.py`: contiene las tres funciones que se pueden llamar desde el cliente.

El archivo `esquema.jpeg` muestra cómo se reparten estas tareas entre el cliente y el servidor.

## Qué operaciones probamos

- `info_imagen(nombre)`: devuelve el nombre del archivo y unos datos de ejemplo: ancho `1920`, alto `1080` y formato `JPEG`.
- `escala_grises(nombre)`: devuelve un texto indicando que la imagen se ha procesado en escala de grises.
- `redimensionar(nombre, width, height)`: devuelve el nombre del archivo y las dimensiones solicitadas.

Estas funciones simulan el trabajo con imágenes: no abren ni modifican archivos reales. No hace falta tener `pepito.jpg` para ejecutar el ejemplo.

## Carpetas de la práctica

- `base`: contiene el punto de partida, con partes pendientes de implementar.
- `v1.0`: contiene la implementación del cliente RPC, el registro y la ejecución de funciones, las respuestas de error y la atención de peticiones mediante hilos.

En `v1.0/app.py` se prueban las tres operaciones válidas. Queda indicado en un comentario probar también una función inexistente y llamadas con argumentos incorrectos. El servidor devuelve errores en estos casos, aunque el cliente los muestra con el mensaje genérico «Error desde el otro lado».

## Cómo ejecutarlo

Necesitamos Python 3. Todas las librerías utilizadas vienen incluidas con Python.

Desde `4_rpc_img`, arrancamos el servidor:

```bash
python3 v1.0/server.py
```

En otra terminal, también desde `4_rpc_img`, ejecutamos la aplicación:

```bash
python3 v1.0/app.py
```

La aplicación muestra la información simulada de `pepito.jpg`, el mensaje de escala de grises y las dimensiones `800 × 600`, y termina. Cada llamada abre una conexión TCP nueva. El servidor sigue esperando peticiones hasta que lo paramos con `Ctrl+C`.
