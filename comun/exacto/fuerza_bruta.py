"""Fuerza bruta, portada de `crear_mochila.py` del TP1.

Explora las 2^n combinaciones sin poda. En el TP1 devolvia solo el valor; aca
devuelve tambien la seleccion.

Ojo con el detalle heredado: una rama que se pasa de capacidad devuelve valor 0
en la base, no `-inf`. Es correcto solo porque los beneficios son no negativos
(una rama infactible nunca puede superar a una factible de valor 0). Si alguna
vez se admiten beneficios negativos, hay que cambiarlo por `-inf`.

Complejidad: O(2^n) tiempo, O(n) espacio de recursion (el TP1 lo llamaba
"espacio O(n)" con razon: no guarda las combinaciones).
"""

from __future__ import annotations

from ..solucion import Solucion


def resolver(inst, traza: list[str] | None = None) -> Solucion:
    """Maximo beneficio por enumeracion completa."""
    n = inst.n
    pesos, beneficios, capacidad = inst.pesos, inst.beneficios, inst.capacidad
    if traza is not None:
        traza.append(f"n={n}: se exploran hasta {2 ** n} combinaciones")

    def explorar(i: int, peso: int, valor: int):
        if i == n:
            if peso <= capacidad:
                return valor, []
            if traza is not None:
                traza.append(f"hoja infactible: peso {peso} > {capacidad}")
            return 0, []

        valor_sin, sel_sin = explorar(i + 1, peso, valor)
        valor_con, sel_con = explorar(i + 1, peso + pesos[i], valor + beneficios[i])
        if valor_con >= valor_sin:
            return valor_con, [i] + sel_con
        return valor_sin, sel_sin

    valor, seleccion = explorar(0, 0, 0)
    seleccion.sort()
    return Solucion(valor=valor, seleccion=seleccion, traza=traza)
