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
    """Útil para comprobar posteriormente la concurrencia."""
    time.sleep(segundos)
    return segundos


# TODO (alumno):
# Añadir al menos dos procedimientos remotos adicionales.
