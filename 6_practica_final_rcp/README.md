# Práctica 1 | Enunciado | Desarrollo de un sistema RPC sobre una instancia EC2

## Objetivo

Construir una pequeña capa RPC en Python sobre TCP.

- El cliente se ejecuta en el ordenador del alumno.
- El servidor se ejecuta en una instancia Amazon EC2.
- El intercambio de mensajes usa JSON.
- No se permite utilizar frameworks RPC (gRPC, RPyC, Pyro, etc.).

## Estructura proporcionada

```text
practica_rpc/
├── client/
│   ├── client_example.py
│   └── rpc_client.py
├── server/
│   ├── server.py
│   ├── procedures.py
│   └── rpc_server.py
├── common/
│   └── protocol.py
├── tests/
│   └── test_rpc.py
└── README.md
```

## Qué está hecho

Se proporciona:

1. Estructura inicial del proyecto.
2. Utilidades básicas para enviar y recibir mensajes JSON sobre TCP.
3. Un servidor TCP mínimo que acepta una conexión y muestra el mensaje recibido.
4. Algunas funciones remotas de ejemplo.
5. Un cliente de ejemplo.
6. Pruebas básicas del protocolo.
7. Indicaciones de despliegue en EC2.

## Qué debe implementar el alumno

El alumno debe completar:

- `RPCClient.call()`.
- El dispatcher del servidor.
- El registro y ejecución de procedimientos.
- La gestión de errores.
- Los timeouts.
- La concurrencia.
- Al menos dos procedimientos remotos adicionales.
- La integración completa entre cliente local y servidor EC2.

## Puesta en marcha rápida

### 1. Servidor local

Desde la raíz del proyecto:

```bash
python -m server.server
```

### 2. Cliente local

En otra terminal:

```bash
python -m client.client_example
```

El código inicial solo demuestra el envío de un mensaje JSON. La capa RPC todavía no está implementada.

## Configuración básica en EC2

1. Crear una instancia Linux en AWS EC2.
2. Permitir tráfico TCP de entrada al puerto elegido, por ejemplo `5000`.
3. Conectarse por SSH.
4. Copiar esta carpeta a la instancia.
5. Ejecutar:

```bash
python -m server.server
```

6. En el cliente, sustituir `127.0.0.1` por la IP pública o DNS público de la instancia EC2.

> No expongas puertos innecesarios y limita el origen de las reglas del Security Group siempre que sea posible.

## Formato de mensajes esperado

Petición:

```json
{
  "function": "sumar",
  "args": [4, 7]
}
```

Respuesta correcta:

```json
{
  "status": "ok",
  "result": 11
}
```

Respuesta de error:

```json
{
  "status": "error",
  "error": "PROCEDURE_NOT_FOUND"
}
```

## Restricciones

- Usar Python 3.10 o superior.
- Usar TCP.
- Usar JSON.
- No usar frameworks RPC.
- Mantener separado el código de aplicación de la lógica de comunicación.

# Mi solución para para el desarrollo de un sistema RPC sobre una instancia EC2

Nombre: Stefan Trifan | Fecha: 28 Oct 2026

### rpc_server

En primer lugar, hemos desarrollado la clase `RPCServer`, que se encarga de gestionar los procedimientos remotos disponibles en el servidor. Esta clase cuenta principalmente con tres métodos: `__init__`, `register` y `dispatch`.

- El método `__init__` inicializa el objeto `RPCServer` y crea el atributo privado `_procedures`. Este atributo es un diccionario clave-valor en el que las claves son cadenas de texto con el nombre de los procedimientos y los valores son las funciones asociadas a cada uno de ellos.
- El método `register` permite registrar nuevas funciones en el servidor. Recibe el nombre con el que queremos identificar el procedimiento y la función que queremos asociar a dicho nombre. Antes de añadirla al diccionario `_procedures`, se comprueba mediante `callable()` que el objeto recibido sea realmente ejecutable. Si no lo es, se genera un error.
- Por último, el método `dispatch` se encarga de procesar las peticiones que llegan al servidor. Estas peticiones son diccionarios que indican el nombre de la función que se quiere ejecutar y los argumentos que deben pasarse a dicha función. Por tanto, el cliente no envía la función como tal, sino que indica qué procedimiento quiere ejecutar y con qué argumentos.

`dispatch` comprueba que el formato de la petición sea correcto y que el procedimiento solicitado se encuentre registrado en `_procedures`. Si todo es correcto, localiza la función correspondiente, delega en ella la ejecución y devuelve el resultado obtenido. Si se produce algún problema, como solicitar un procedimiento inexistente o utilizar argumentos incorrectos, se devuelve una respuesta de error.

### rpc_client

A continuación, hemos desarrollado la clase `RPCClient`, que se encarga de abstraer los detalles de la comunicación remota. El cliente únicamente necesita conocer el nombre de la operación que quiere ejecutar y los parámetros que desea enviar. A partir de estos datos, `RPCClient` se encarga de realizar todo el proceso de comunicación y devolver el resultado, sin que el cliente tenga que conocer los detalles del protocolo, la conversión a JSON o la configuración de la conexión.

Esta clase cuenta principalmente con dos métodos:

- **Constructor (`__init__`)**: recibe el `host`, el `puerto` y el `timeout`. El `host` y el puerto indican dónde se encuentra el servidor RPC, mientras que el `timeout` establece el tiempo máximo que el cliente puede permanecer esperando durante una operación de comunicación antes de considerar que se ha producido un error. Si no se especifica, se utiliza un valor de 5 segundos por defecto.
- **Método `call`**: recibe el nombre de la función que se quiere ejecutar y sus argumentos. A partir de ellos construye la petición RPC, representada mediante un diccionario de Python que contiene el nombre de la función y la lista de argumentos.

    Una vez creada la petición, `call` abre una conexión TCP con el servidor y configura el `timeout` establecido anteriormente. Para enviar la petición utiliza la función `send_json`, a la que se le proporciona el socket y el diccionario con la petición. Esta función proporciona otra capa de abstracción, ya que se encarga internamente de convertir el diccionario a JSON, codificarlo y enviarlo a través del socket mediante `sendall`.

    La respuesta se obtiene mediante `recv_json`, que realiza el proceso inverso: recibe los datos enviados por el servidor y los transforma de nuevo en una estructura de Python que pueda ser procesada por el cliente.

    Por último, `RPCClient` también se encarga de gestionar los posibles fallos de comunicación, evitando que el cliente pueda quedarse bloqueado indefinidamente. Si la respuesta recibida tiene un estado `ok`, el método devuelve directamente el resultado de la operación. En caso contrario, identifica el error devuelto por el servidor y genera el error correspondiente para informar al cliente de lo ocurrido.


### procedures

El archivo `procedures.py` contiene las funciones que el servidor puede ejecutar de forma remota. Inicialmente incluye cuatro procedimientos sencillos: `sumar`, `multiplicar`, `potencia` y `tarea_lenta`. Esta última simplemente espera durante el número de segundos indicado, por lo que también resulta útil para realizar pruebas de timeout y concurrencia.

Además de estas funciones, hemos añadido dos procedimientos propios: `factorial_recursivo`, que calcula de forma recursiva el factorial de un número, y `validar_ipv4`, que comprueba si una dirección IPv4 tiene un formato válido.

Por tanto, este archivo se limita a definir la lógica de las operaciones que estarán disponibles en el sistema RPC. Como veremos más adelante, `server.py` se encarga de registrar estos procedimientos en `RPCServer`. Cuando llega una petición del cliente, el `dispatcher` identifica el procedimiento solicitado dentro del registro y ejecuta la función correspondiente con los argumentos recibidos.

### server

El archivo `server.py` es el encargado de poner en funcionamiento nuestro servidor TCP y conectar las distintas partes del sistema RPC. En primer lugar, creamos una instancia de `RPCServer` y registramos en ella todos los procedimientos que hemos definido en `procedures.py`, asociando el nombre de cada procedimiento con su función correspondiente.

A continuación, creamos un socket TCP utilizando `AF_INET` y `SOCK_STREAM`, lo asociamos al puerto `5001` mediante `bind()` y lo ponemos en modo escucha con `listen()`. Para el servidor utilizamos la dirección `0.0.0.0`, lo que nos permite aceptar conexiones procedentes de cualquier interfaz de red.

El servidor se mantiene continuamente a la espera de nuevas conexiones mediante `accept()`. Cada vez que aceptamos una conexión, la asignamos a un nuevo hilo utilizando `threading.Thread`. De esta forma, podemos atender a varios clientes al mismo tiempo sin bloquear el hilo principal del servidor.

Cada uno de estos hilos ejecuta la función `atender_cliente`, donde recibimos la petición mediante `recv_json` y la pasamos al `dispatcher` de `RPCServer`, que se encarga de ejecutar el procedimiento solicitado. Una vez obtenido el resultado, enviamos la respuesta al cliente mediante `send_json`.

De esta manera, utilizamos `server.py` como punto de unión entre la comunicación TCP, nuestro sistema RPC y los procedimientos disponibles. Además, gracias al uso de hilos, conseguimos que el servidor pueda gestionar varias conexiones de forma concurrente.

### client_example

El archivo `client_example.py` representa nuestra aplicación cliente y lo utilizamos como punto de entrada para realizar las llamadas RPC. En primer lugar, definimos la dirección `HOST` del servidor y el puerto `5001` al que nos conectamos. Durante las pruebas locales utilizamos `127.0.0.1` y, posteriormente, lo sustituimos por la dirección IP pública de nuestra instancia EC2.

Dentro de `main()` creamos una instancia de `RPCClient`, indicando el host y el puerto del servidor. A partir de ahí, podemos ejecutar procedimientos remotos mediante el método `call`, indicando únicamente el nombre del procedimiento que queremos ejecutar y sus argumentos.

Por ejemplo, al realizar la llamada `rpc.call("sumar", 4, 7)`, solicitamos al servidor que ejecute el procedimiento `sumar` con los valores `4` y `7`. Toda la comunicación necesaria la gestiona `RPCClient`, por lo que en `client_example.py` no tenemos que trabajar directamente con los sockets, los mensajes JSON ni las respuestas recibidas del servidor.

En este archivo realizamos llamadas a los distintos procedimientos que hemos registrado, como `sumar`, `multiplicar`, `potencia`, `factorial_recursivo` o `validar_ipv4`. De esta forma, podemos comprobar de manera sencilla el funcionamiento completo de nuestro sistema RPC desde el lado del cliente.

### test_rpc

En el archivo `test_rpc.py` realizamos pruebas automáticas utilizando `unittest` para comprobar que el sistema funciona correctamente. Por un lado, probamos el protocolo verificando que un mensaje enviado mediante `send_json` pudiera recuperarse correctamente con `recv_json`. Por otro lado, probamos el `dispatcher`, donde registramos el procedimiento `sumar` y comprobamos que al ejecutar `sumar(4, 7)` obtuviéramos como resultado `11`.

Para ejecutar las pruebas utilizamos el comando `python -m unittest discover -s tests`. Ambas pruebas se completaron correctamente, por lo que pudimos comprobar que tanto el protocolo como el `dispatcher` funcionaban según lo esperado.

### Protocol

El archivo `protocol.py` contiene las funciones que utilizamos para enviar y recibir mensajes entre el cliente y el servidor. Para la comunicación elegimos JSON, ya que permite representar de forma sencilla tanto las peticiones como las respuestas mediante diccionarios.

La función `send_json` convierte el diccionario de Python a formato JSON, lo codifica en bytes y lo envía a través del socket. Antes de enviar el contenido, se mandan 4 bytes con la longitud total del mensaje. Esto permite que el receptor sepa exactamente cuántos bytes tiene que leer.

Por otro lado, `recv_json` realiza el proceso contrario. Primero lee los 4 bytes correspondientes a la longitud del mensaje y, a partir de ese valor, recibe el contenido completo. Finalmente, transforma el JSON recibido de nuevo en un diccionario de Python.

### Despliegue en Amazon EC2

Después de comprobar que el sistema funcionaba correctamente en local, desplegamos el servidor utilizando una instancia de Amazon EC2 que ya habíamos creado y configurado previamente en clase. Por tanto, no fue necesario crear una nueva instancia, sino adaptar la existente para permitir la comunicación con nuestro servidor RPC.

Configuramos el servidor para escuchar en `0.0.0.0:5001` y añadimos al grupo de seguridad de la instancia una nueva regla de entrada para permitir conexiones TCP a través del puerto `5001`.

Una vez configurado el acceso, cambiamos en el cliente la dirección local `127.0.0.1` por la dirección IP pública de la instancia EC2. De esta manera, pudimos ejecutar el cliente desde nuestro equipo local y realizar correctamente las llamadas RPC al servidor alojado en AWS.

### Decisiones de diseño

Para la comunicación entre cliente y servidor decidimos utilizar sockets TCP, principalmente porque necesitábamos una conexión fiable y orientada a conexión. Para el intercambio de mensajes usamos JSON.

También añadimos un `timeout` para evitar que el cliente se quede bloqueado indefinidamente en caso de que el servidor no responda. Además, el servidor utiliza hilos para gestionar las conexiones. Cada cliente se atiende en un hilo independiente, lo que permite procesar varias conexiones de forma simultánea.