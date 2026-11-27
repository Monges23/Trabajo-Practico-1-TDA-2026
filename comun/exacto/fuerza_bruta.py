"""Fuerza bruta, portada de `crear_mochila.py` del TP1.

Explora las 2^n combinaciones sin poda. En el TP1 devolvia solo el valor; aca
devuelve tambien la seleccion.

Ojo con un detalle que el TP1 no exponia: una rama que se pasa de capacidad
vale 0 pero **no** vale seleccion vacia. Mientras solo se devolvia el valor
alcanzaba con devolver 0 (los beneficios son no negativos, asi que una rama
infactible nunca supera a una factible), pero al sumar la seleccion el
maximo entre "no tomar" y "tomar" empataba en 0 y se quedaba con la rama
infactible. Por eso la hoja infactible devuelve `-inf` y el desempate nunca la
elige. La seleccion vacia siempre es factible, asi que el resultado nunca queda
en `-inf` para `w >= 0`.

Complejidad: O(2^n) tiempo, O(n) espacio de recursion (el TP1 lo llamaba
"espacio O(n)" con razon: no guarda las combinaciones).

Contrato de datos (el de `comun/parser_mochila.py`): `elems[i]` es el par
`(peso, beneficio)`, `n` la cantidad de elementos y `w` la capacidad.
"""

from __future__ import annotations


def resolver(elems, n: int, w: int, traza: list[str] | None = None) -> tuple[int, list[int]]:
    """Maximo beneficio por enumeracion completa. Devuelve `(valor, seleccion)`."""
    if traza is not None:
        traza.append(f"n={n}: se exploran hasta {2 ** n} combinaciones")

    infactible = float("-inf")

    def explorar(i: int, peso: int, valor: int) -> tuple[float, list[int]]:
        if i == n:
            if peso <= w:
                return valor, []
            if traza is not None:
                traza.append(f"hoja infactible: peso {peso} > {w}")
            return infactible, []

        peso_i, beneficio_i = elems[i]
        valor_sin, sel_sin = explorar(i + 1, peso, valor)
        valor_con, sel_con = explorar(i + 1, peso + peso_i, valor + beneficio_i)
        if valor_con >= valor_sin:
            return valor_con, [i] + sel_con
        return valor_sin, sel_sin

    valor, seleccion = explorar(0, 0, 0)
    seleccion.sort()
    return valor, seleccion
