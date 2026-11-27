"""Backtracking con poda, portado de `crear_mochila.py` del TP1.

Poda heredada del TP1: se corta cuando el beneficio acumulado mas la suma de
beneficios de los elementos restantes (`sufijo`) no supera al mejor encontrado.
Es una cota valida pero floja, porque ignora los pesos. La version del TP1 no
ordena los elementos por beneficio/peso: si se ordenaran antes de explorar, la
misma cota podaria mucho mas y bajaria el arbol explorado. Queda igual que en el
TP1 para que la comparacion de P4 sea contra el mismo algoritmo que se entrego.

Complejidad: O(2^n) en el peor caso; la poda solo mejora el promedio.

Contrato de datos (el de `comun/parser_mochila.py`): `elems[i]` es el par
`(peso, beneficio)`, `n` la cantidad de elementos y `w` la capacidad.
"""

from __future__ import annotations


def resolver(elems, n: int, w: int, traza: list[str] | None = None) -> tuple[int, list[int]]:
    """Maximo beneficio por backtracking con poda por cota de sufijo."""
    sufijo = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        sufijo[i] = sufijo[i + 1] + elems[i][1]

    mejor = 0
    mejor_seleccion: list[int] = []
    decision = [False] * n
    nodos = 0
    podas = 0

    def explorar(i: int, peso: int, valor: int) -> None:
        nonlocal mejor, mejor_seleccion, nodos, podas
        nodos += 1
        if valor > mejor:
            mejor = valor
            mejor_seleccion = [j for j in range(i) if decision[j]]
        if i == n:
            return
        if valor + sufijo[i] <= mejor:
            podas += 1
            return
        peso_i = elems[i][0]
        if peso + peso_i <= w:
            decision[i] = True
            explorar(i + 1, peso + peso_i, valor + elems[i][1])
            decision[i] = False
        explorar(i + 1, peso, valor)

    explorar(0, 0, 0)
    if traza is not None:
        traza.append(f"n={n}: nodos explorados={nodos} podas={podas}")

    mejor_seleccion.sort()
    return mejor, mejor_seleccion
