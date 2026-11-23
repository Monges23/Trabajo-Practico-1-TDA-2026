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
"""

from __future__ import annotations

from ..solucion import Solucion


def resolver(inst, traza: list[str] | None = None) -> Solucion:
    """Optimo por PD con tabla completa y reconstruccion de la seleccion."""
    n, W = inst.n, inst.capacidad
    pesos, beneficios = inst.pesos, inst.beneficios

    tabla = [[0] * (W + 1) for _ in range(n + 1)]
    for elem in range(1, n + 1):
        valor = beneficios[elem - 1]
        peso = pesos[elem - 1]
        fila_previa, fila = tabla[elem - 1], tabla[elem]
        for w in range(1, W + 1):
            if peso <= w:
                con = valor + fila_previa[w - peso]
                fila[w] = con if con > fila_previa[w] else fila_previa[w]
            else:
                fila[w] = fila_previa[w]

    seleccion: list[int] = []
    w = W
    for elem in range(n, 0, -1):
        if tabla[elem][w] != tabla[elem - 1][w]:
            seleccion.append(elem - 1)
            w -= pesos[elem - 1]
    seleccion.sort()

    if traza is not None:
        traza.append(
            f"n={n} W={W}: tabla de {(n + 1) * (W + 1)} celdas, "
            f"seleccion de {len(seleccion)} elementos"
        )
    return Solucion(valor=tabla[n][W], seleccion=seleccion, traza=traza)


def valor_compacto(inst) -> int:
    """Optimo por PD con vector de O(W) en espacio (sin seleccion)."""
    W = inst.capacidad
    dp = [0] * (W + 1)
    for peso, beneficio in zip(inst.pesos, inst.beneficios):
        for w in range(W, peso - 1, -1):
            candidato = dp[w - peso] + beneficio
            if candidato > dp[w]:
                dp[w] = candidato
    return dp[W]


def peso_minimo_para_beneficio(inst, objetivo: int) -> float:
    """Formulacion dual: minimo peso necesario para lograr beneficio >= objetivo.

    Devuelve `float('inf')` si no hay combinacion que llegue al objetivo.
    No es un solver del optimo; sirve para el estudio O(n*B) del informe.
    """
    inf = float("inf")
    tabla = [[inf] * (objetivo + 1) for _ in range(inst.n + 1)]
    for i in range(inst.n + 1):
        tabla[i][0] = 0

    for elem in range(1, inst.n + 1):
        valor = inst.beneficios[elem - 1]
        peso = inst.pesos[elem - 1]
        for b in range(1, objetivo + 1):
            con = peso + tabla[elem - 1][max(0, b - valor)]
            sin = tabla[elem - 1][b]
            tabla[elem][b] = con if con < sin else sin

    return tabla[inst.n][objetivo]
