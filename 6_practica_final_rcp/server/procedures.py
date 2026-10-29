"""Procedimientos remotos de ejemplo proporcionados."""

from __future__ import annotations
import time

def sumar(a, b):
    return a + b

def multiplicar(a, b):
    return a * b

def potencia(a, b):
    return a ** b

def tarea_lenta(segundos):
    # Útil para comprobar posteriormente la concurrencia.
    time.sleep(segundos)
    return segundos

# done (alumno):
# Añadir al menos dos procedimientos remotos adicionales.

def factorial_recursivo(n):
    if not isinstance(n, int):
        raise TypeError("El numero debe ser un entero")
    if n < 0:
        raise ValueError("El numero no puede ser negativo")
    
    # caso base
    if n == 0 or n == 1:
        return 1

    # llamada recursiva
    return n * factorial_recursivo(n - 1)


def validar_ipv4(ip):
    if not isinstance(ip, str):
        return False

    bloques = ip.split(".")

    if len(bloques) != 4:
        return False

    for bloque in bloques:
        if not bloque.isdigit():
            return False

        numero = int(bloque)

        if numero < 0 or numero > 255:
            return False

    return True