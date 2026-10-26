# Ejercicio 5: hablar con un servidor

Este es un ejercicio que hicimos en clase. El profesor ejecutaba el código de `server.py` en una instancia de **Amazon EC2** y nosotros, como estudiantes, teníamos que crear un cliente para hablar con otros compañeros a través de ese servidor. Lo que subo aquí es mi solución.

El objetivo era empezar enviando y recibiendo mensajes, después hacer ambas cosas a la vez y, por último, enviar un mensaje a un compañero concreto.

## Conceptos que se trabajan

- **Cliente-servidor y sockets TCP:** los clientes se conectan a una IP y un puerto; el servidor recibe los mensajes y los reenvía.
- **JSON:** los mensajes llevan campos como `action`, `name` y `text` para indicar qué queremos hacer.
- **Hilos (`threading`):** permiten recibir mensajes mientras seguimos escribiendo con `input()`. El servidor también utiliza un hilo por cliente.
- **Identificación y envío de mensajes:** `mynameis` registra nuestro nombre, `broadcast` envía a todos y `messageto` envía a un compañero por su nombre.

## Archivos

`base/` contiene el código inicial del servidor y el enunciado, con el cliente vacío. En `v1.0/` está mi solución:

- `server.py`: acepta conexiones y reparte los mensajes.
- `client.py`: se identifica como `steve` y envía mensajes a todos los clientes conectados, incluido él mismo.
- `compi.py`: permite probar el envío de mensajes privados a `steve`.

Los dos clientes pueden recibir mensajes mientras esperan que escribamos.

## Cómo probarlo

Hace falta **Python 3**, sin instalar librerías adicionales. Desde la carpeta `5_ej_hablar_con_servidor`, abrimos tres terminales y ejecutamos, en este orden, un programa en cada una:

```bash
python3 v1.0/server.py
```

```bash
python3 v1.0/client.py
```

```bash
python3 v1.0/compi.py
```

Al escribir en `client.py` y pulsar Intro, el mensaje aparece en ambos clientes. Al escribir en `compi.py`, el mensaje solo llega a `client.py`, que está registrado como `steve`. Los mensajes recibidos aparecen como JSON después de `Respuesta:`.

La configuración actual usa `127.0.0.1` y el puerto `5001` para probarlo en el mismo ordenador. En clase, `HOST` era la IP del servidor en EC2. Para usar un servidor remoto, hay que cambiar `HOST` en los clientes y permitir el acceso al puerto `5001` en el servidor.

Los clientes tienen un tiempo de espera de 30 segundos: si no reciben mensajes durante ese tiempo, el hilo receptor termina y hay que reiniciarlos para seguir recibiendo. Para cerrar los programas, pulsamos `Ctrl+C` en cada terminal.
