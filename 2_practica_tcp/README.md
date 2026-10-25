# Práctica 2: comunicación con TCP

En esta práctica estamos aprendiendo a comunicar un cliente y un servidor usando sockets TCP en Python. Primero se establece una conexión y después se usa esa misma conexión para enviar mensajes y recibir respuestas.

En las tres versiones, el servidor escucha en el puerto `5001` y el cliente se conecta a `127.0.0.1` (nuestro propio ordenador). Usamos `sendall()` para enviar bytes y `recv()` para recibirlos. Con `encode()` pasamos de texto a bytes y con `decode()` volvemos a texto.

## Las tres versiones

### v1.0: enviar y responder un saludo

El cliente envía «Hola servidor» cada segundo y el servidor responde «Hola cliente». Así practicamos cómo abrir una conexión TCP y mantener un intercambio de mensajes.

El servidor atiende a un cliente cada vez. Hasta que ese cliente se desconecta, no pasa a atender al siguiente.

### v2.0: enviar peticiones con JSON

Pasamos de enviar solo un saludo a enviar datos con una estructura. Usamos JSON para indicar qué le pedimos al servidor:

- `message`: el servidor responde con un saludo y un estado `ok`.
- `time`: el servidor responde con su hora actual y un estado `ok`.
- Si el tipo de petición no es conocido, responde con un estado `error` y «Orden desconocida».

El cliente repite cada dos segundos un ciclo con una petición de saludo y otra de hora, y muestra las respuestas. `json.dumps()` convierte los diccionarios a texto JSON y `json.loads()` permite al servidor convertir ese texto en diccionarios.

Como en la versión anterior, el servidor sigue atendiendo a un solo cliente cada vez.

### v3.0: atender a varios clientes a la vez

Mantenemos las mismas peticiones y respuestas JSON de la versión 2. El cambio está en el servidor: ahora crea un hilo con `threading.Thread` para atender cada conexión.

Un hilo permite atender a un cliente mientras el servidor sigue aceptando otros. Para comprobarlo, podemos ejecutar varios clientes en terminales distintas y ver que todos reciben respuesta sin esperar a que los demás se desconecten.

| Versión | Qué intercambiamos | Cómo atiende el servidor |
| --- | --- | --- |
| v1.0 | Saludos en texto | Un cliente cada vez |
| v2.0 | Peticiones y respuestas JSON: saludo y hora | Un cliente cada vez |
| v3.0 | Las mismas peticiones y respuestas JSON | Varios clientes a la vez, con un hilo por cliente |

## Cómo ejecutarlo

Necesitamos Python 3. Todas las librerías utilizadas vienen incluidas con Python.

Desde `2_practica_tcp`, arrancamos el servidor de la versión que queramos probar. Por ejemplo, para la versión 3:

```bash
python3 v3.0/server.py
```

En otra terminal, también desde `2_practica_tcp`, ejecutamos su cliente:

```bash
python3 v3.0/client.py
```

Para probar las otras versiones, cambiamos `v3.0` por `v1.0` o `v2.0` en ambos comandos. Ejecutamos solo un servidor a la vez, porque todos usan el mismo puerto. Los programas se repiten hasta que los paramos con `Ctrl+C`; el cliente tiene una espera máxima de 3 segundos para conectar y para las operaciones de comunicación.

El archivo `esquema.jpeg` contiene un dibujo de la comunicación TCP entre clientes y servidor.

Como simplificación de la práctica, cada envío se lee con un solo `recv(4096)`. TCP entrega un flujo de bytes y no separa los mensajes: en una aplicación más completa tendríamos que indicar dónde termina cada mensaje y acumular los datos hasta recibirlo entero.
