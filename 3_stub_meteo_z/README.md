# Práctica 3: un stub para consultar el tiempo

En esta práctica estamos aprendiendo a usar un **stub**: una clase que oculta la comunicación con el servidor. Así, la aplicación puede llamar a métodos como `m.temperatura('Madrid')` sin tener que gestionar sockets ni mensajes JSON directamente.

Los datos del tiempo están escritos en el código como ejemplos; no se consultan en un servicio meteorológico real.

## Qué hace cada archivo

- `app.py`: utiliza `MeteoStub` para consultar los datos y mostrarlos por pantalla.
- `meteo_stub.py`: abre una conexión TCP, envía la operación y sus datos en JSON, recibe la respuesta y devuelve el resultado. Si el servidor responde con un error, lanza una excepción `RuntimeError`.
- `server.py`: escucha en `127.0.0.1:5002`, recibe la petición, ejecuta la operación y devuelve una respuesta JSON.

Cada consulta abre una conexión nueva que se cierra al terminar. El servidor sigue esperando más consultas.

La carpeta `base` contiene el punto de partida del ejercicio, con métodos pendientes de implementar que lanzan `NotImplementedError`. Las dos versiones desarrolladas son `v1.0` y `v2.0`.

## Diferencias entre las versiones

### v1.0: consultar los datos de una ciudad

Implementamos el stub y las funciones del servidor. La aplicación hace tres consultas para Madrid:

- Temperatura: `21`.
- Humedad: `10`.
- Pronóstico: `Maremoto`.

Las peticiones incluyen la operación y la ciudad. Si la ciudad no está disponible o la operación no existe, el servidor devuelve un error.

### v2.0: elegir el día de la temperatura

Añadimos el parámetro `dia` a la consulta de temperatura. El cambio pasa por la aplicación, el stub y el servidor:

- `m.temperatura('Madrid', 'hoy')` devuelve `21`.
- `m.temperatura('Madrid', 'manana')` devuelve `28`.

El stub envía también el campo `dia` en el JSON y el servidor lo utiliza para elegir el resultado. La humedad y el pronóstico siguen funcionando igual que en la versión 1, sin elegir día.

El archivo `v2.0/enunciado.txt` pide mostrar el pronóstico del próximo día. En el código actual, la consulta que se ha ampliado para distinguir entre hoy y mañana es la **temperatura**; `pronostico()` sigue devolviendo el mismo texto.

| Versión | Consulta de temperatura | Humedad y pronóstico |
| --- | --- | --- |
| v1.0 | Solo recibe la ciudad | Solo reciben la ciudad |
| v2.0 | Recibe la ciudad y el día (`hoy` o `manana`) | Siguen recibiendo solo la ciudad |

## Cómo ejecutarlo

Necesitamos Python 3. No hace falta instalar librerías adicionales.

Desde `3_stub_meteo_z`, arrancamos el servidor de la versión que queramos probar. Por ejemplo:

```bash
python3 v2.0/server.py
```

En otra terminal, también desde `3_stub_meteo_z`, ejecutamos la aplicación de esa misma versión:

```bash
python3 v2.0/app.py
```

La aplicación muestra `21`, `28`, `10` y `Maremoto`, cada resultado en una línea, y termina. El servidor sigue activo hasta que lo paramos con `Ctrl+C`.

Para probar la versión 1, cambiamos `v2.0` por `v1.0` en ambos comandos. Ejecutamos solo un servidor a la vez, porque las dos versiones usan el puerto `5002`.
