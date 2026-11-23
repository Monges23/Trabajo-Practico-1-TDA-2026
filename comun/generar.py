"""Generador de instancias, portado de `crear_mochila.py` del TP1.

El TP1 generaba con `randint` sin semilla: dos corridas daban instancias
distintas y los resultados del informe no se podian reproducir. Aca el
generador es `random.Random(semilla)`, asi que una instancia queda determinada
por (n, semilla) y se puede regenerar igual dentro de seis meses.

Distribucion del TP1 (se conserva para que los sets nuevos sean comparables
con los del TP1):

    peso      ~ U[1, 200]
    beneficio ~ U[1, 1000]
    W         = n * 50

Con esos valores, W cubre aproximadamente la mitad del peso total de los
elementos (suma esperada de pesos = n * 100.5), o sea que la mochila no es ni
trivial ni imposible.

Las familias correlacionadas (debilmente, fuertemente, subset-sum) que sugiere
`datos/` NO estan implementadas: cambian la conclusion del analisis (en las
fuertemente correlacionadas la cota de relajacion lineal se debilita) y sus
parametros son una decision de quien las use, no algo que se pueda inventar
aca.
"""

from __future__ import annotations

import random
from pathlib import Path

from .instancia import Instancia, escribir


def generar(
    n: int,
    semilla: int | None = None,
    peso_max: int = 200,
    beneficio_max: int = 1000,
    capacidad_por_elemento: int = 50,
) -> Instancia:
    """Instancia con la distribucion del TP1, reproducible por semilla."""
    if n <= 0:
        raise ValueError(f"n invalido: {n}")
    rnd = random.Random(semilla)
    pesos = [rnd.randint(1, peso_max) for _ in range(n)]
    beneficios = [rnd.randint(1, beneficio_max) for _ in range(n)]
    capacidad = n * capacidad_por_elemento
    return Instancia(pesos, beneficios, capacidad, nombre=f"mochila{n}_s{semilla}")


def generar_archivo(
    n: int,
    ruta: str | Path,
    semilla: int | None = None,
    **opciones,
) -> Instancia:
    """Genera una instancia y la deja escrita en `ruta`."""
    inst = generar(n, semilla=semilla, **opciones)
    escribir(inst, ruta)
    return inst
