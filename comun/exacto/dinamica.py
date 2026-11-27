"""Programacion dinamica del TP1: tres variantes, tres usos distintos.

1. `resolver`        -- tabla completa O(n*W) en tiempo y espacio. Es la que el
                        TP1 presento en el informe, con reconstruccion de la
                        seleccion (el TP1 devolvia solo el valor).
2. `valor_compacto`  -- vector de O(W) en espacio, sin reconstruccion: es la
                        unica que escala a las instancias grandes del TP1
                        (n=20000 con W=10^6 no entra en una tabla de n*W).
3. `peso_minimo_para_beneficio` -- formulacion dual del TP1
                        (`tp1/mochila_alt.py`): minimo peso para lograr al menos
                        B de beneficio, O(n*B). No resuelve el optimo de la
                        mochila; el TP1 la uso para comparar la curva de
                        complejidad O(n*W) contra O(n*B).

Cuidado con los tamanos: la tabla completa usa n*(W+1) enteros de Python (~28
bytes cada uno), o sea que n=1000 con W=50000 ya son ~1,4 GB. Para medir tiempos
grandes usar `valor_compacto`.

Contrato de datos (el de `comun/parser_mochila.py`): `elems[i]` es el par
`(peso, beneficio)`, `n` la cantidad de elementos y `w` la capacidad.
"""

from __future__ import annotations


def resolver(elems, n: int, w: int, traza: list[str] | None = None) -> tuple[int, list[int]]:
    """Optimo por PD con tabla completa y reconstruccion de la seleccion."""
    tabla = [[0] * (w + 1) for _ in range(n + 1)]
    for elem in range(1, n + 1):
        peso, valor = elems[elem - 1]
        fila_previa, fila = tabla[elem - 1], tabla[elem]
        for cap in range(1, w + 1):
            if peso <= cap:
                con = valor + fila_previa[cap - peso]
                fila[cap] = con if con > fila_previa[cap] else fila_previa[cap]
            else:
                fila[cap] = fila_previa[cap]

    seleccion: list[int] = []
    cap = w
    for elem in range(n, 0, -1):
        if tabla[elem][cap] != tabla[elem - 1][cap]:
            seleccion.append(elem - 1)
            cap -= elems[elem - 1][0]
    seleccion.sort()

    if traza is not None:
        traza.append(
            f"n={n} W={w}: tabla de {(n + 1) * (w + 1)} celdas, "
            f"seleccion de {len(seleccion)} elementos"
        )
    return tabla[n][w], seleccion


def valor_compacto(elems, n: int, w: int) -> int:
    """Optimo por PD con vector de O(W) en espacio (sin seleccion)."""
    dp = [0] * (w + 1)
    for i in range(n):
        peso, beneficio = elems[i]
        for cap in range(w, peso - 1, -1):
            candidato = dp[cap - peso] + beneficio
            if candidato > dp[cap]:
                dp[cap] = candidato
    return dp[w]


def peso_minimo_para_beneficio(elems, n: int, objetivo: int) -> float:
    """Formulacion dual: minimo peso necesario para lograr beneficio >= objetivo.

    Devuelve `float('inf')` si no hay combinacion que llegue al objetivo.
    No es un solver del optimo; sirve para el estudio O(n*B) del informe.
    """
    inf = float("inf")
    tabla = [[inf] * (objetivo + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        tabla[i][0] = 0

    for elem in range(1, n + 1):
        peso, valor = elems[elem - 1]
        for b in range(1, objetivo + 1):
            con = peso + tabla[elem - 1][max(0, b - valor)]
            sin = tabla[elem - 1][b]
            tabla[elem][b] = con if con < sin else sin

    return tabla[n][objetivo]
