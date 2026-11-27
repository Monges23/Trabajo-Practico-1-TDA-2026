"""Programacion lineal, portada de `pl/mochila.py` del TP1.

Decision del grupo para P1: la programacion lineal es el metodo que da la
solucion optima. El TP1 resolvia el modelo con variables binarias y dejaba el
optimo entero; aca el mismo modelo se resuelve con dos categorias de variable:

- `resolver`       -> variables binarias: optimo exacto del 0/1.
- `relajacion`     -> variables continuas: cota superior por relajacion lineal
                      (fraccionaria; la cota entera es `math.floor` del valor).

Tener los dos sobre el mismo modelo es justamente lo que pide P1: la diferencia
entre el valor de la relajacion y el entero es la brecha de integralidad, y el
LP continuo es, ademas, el que tiene solucion cerrada O(n log n) (ordenar por
beneficio/peso y llenar) que hay que mostrar en el pseudocodigo del informe.

DOS APIS DE PULP
El TP1 usaba `pulp.LpVariable.dicts(...)` y `pulp.PULP_CBC_CMD(...)`. PuLP 4 es
una reescritura con nucleo en Rust: se lleva puestas esas dos y ademas NO trae
ningun solver, hay que instalarle un backend (`highspy`). PuLP 3.3 si trae CBC
adentro y ya acepta `add_variable_dicts`, asi que la unica diferencia que
importa es el solver, y es lo que se detecta aca:

    PuLP <= 3   PULP_CBC_CMD (CBC incluido en el paquete)
    PuLP >= 4   HiGHS (necesita highspy instalado aparte)

`add_variable_dicts` se usa cuando existe (3.3 y 4) y si no `LpVariable.dicts`
(2.x). Asi corre con la version que tenga el corrector sin tocar nada.

PuLP se importa dentro de las funciones a proposito: `comun` tiene que poder
importarse sin PuLP instalado, porque las ramas de P2 y P3 no lo usan. Si falta:

    pip install -r requirements.txt

Aviso para P4: el TP1 medía el armado del modelo y el solver por separado
porque el armado, en Python, es overhead que no es del algoritmo. Aca
`resolver_con_tiempos` conserva esa distincion.

Contrato de datos (el de `comun/parser_mochila.py`): `elems[i]` es el par
`(peso, beneficio)`, `n` la cantidad de elementos y `w` la capacidad.
"""

from __future__ import annotations

import time


def _exigir_pulp():
    try:
        import pulp
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            "programacion_lineal necesita PuLP: pip install -r requirements.txt"
        ) from None
    return pulp


def _api(pulp):
    """Devuelve (crear_variables, resolver) para la version de PuLP instalada."""
    if hasattr(pulp.LpProblem, "add_variable_dicts"):  # PuLP >= 3.3

        def crear(problema, cantidad, categoria, **cotas):
            return problema.add_variable_dicts(
                "x", range(cantidad), cat=categoria, **cotas
            )

    else:  # PuLP 2.x

        def crear(problema, cantidad, categoria, **cotas):
            return pulp.LpVariable.dicts("x", range(cantidad), cat=categoria, **cotas)

    # La deteccion que importa es el solver: PuLP <= 3 trae CBC, PuLP 4 no trae
    # ninguno y delega en un backend externo.
    if hasattr(pulp, "PULP_CBC_CMD"):

        def resolver(problema):
            problema.solve(pulp.PULP_CBC_CMD(msg=0))

    else:

        def resolver(problema):
            problema.solve(pulp.HiGHS(msg=False))

    return crear, resolver


def _modelo(elems, n: int, w: int, categoria: str):
    """Modelo de mochila 0/1 con variables de la categoria pedida.

    Para la relajacion las variables continuas llevan `0 <= x <= 1`. Sin el tope
    superior no se relaja el 0/1: se resuelve otro problema, donde cada x_i puede
    crecer hasta agotar la capacidad y el "valor" da varias veces el optimo. Con
    `Binary` las cotas ya vienen implicitas.
    """
    pulp = _exigir_pulp()
    crear, resolver = _api(pulp)
    problema = pulp.LpProblem("mochila", pulp.LpMaximize)
    cotas = {"lowBound": 0, "upBound": 1} if categoria == "Continuous" else {}
    x = crear(problema, n, categoria, **cotas)
    problema += pulp.lpSum(elems[i][1] * x[i] for i in range(n))
    problema += pulp.lpSum(elems[i][0] * x[i] for i in range(n)) <= w
    return pulp, problema, x, resolver


def _seleccion(x, n: int) -> list[int]:
    return [i for i in range(n) if (x[i].value() or 0) > 0.5]


def _beneficio(elems, seleccion) -> int:
    return sum(elems[i][1] for i in seleccion)


def resolver_con_tiempos(elems, n: int, w: int) -> tuple[tuple[int, list[int]], float, float]:
    """Optimo entero. Devuelve ((valor, seleccion), t_armado_modelo, t_solver)."""
    inicio = time.perf_counter()
    pulp, problema, x, resolver_modelo = _modelo(elems, n, w, "Binary")
    t_modelo = time.perf_counter() - inicio
    inicio = time.perf_counter()
    resolver_modelo(problema)
    t_solver = time.perf_counter() - inicio
    seleccion = _seleccion(x, n)
    return (_beneficio(elems, seleccion), seleccion), t_modelo, t_solver


def resolver(elems, n: int, w: int, traza: list[str] | None = None) -> tuple[int, list[int]]:
    """Optimo exacto del 0/1 por programacion lineal entera."""
    _pulp, problema, x, resolver_modelo = _modelo(elems, n, w, "Binary")
    resolver_modelo(problema)
    seleccion = _seleccion(x, n)
    if traza is not None:
        traza.append(
            f"modelo: {n} variables binarias, 1 restriccion de capacidad W={w}"
        )
    return _beneficio(elems, seleccion), seleccion


def relajacion(elems, n: int, w: int) -> float:
    """Valor de la relajacion lineal (cota superior, normalmente fraccionaria).

    La cota entera que se compara en P1 es `math.floor` de este valor, no el
    valor crudo: los beneficios son enteros, asi que el optimo es entero.

    Propiedad util para verificar: la relajacion solo se diferencia del optimo
    en el elemento critico, que queda fraccionario, asi que
    `z_lp - z_optimo <= max(beneficios)`. Si la brecha es mayor, el modelo esta
    mal armado (por ejemplo, sin el tope x <= 1).
    """
    pulp, problema, _x, resolver_modelo = _modelo(elems, n, w, "Continuous")
    resolver_modelo(problema)
    return float(pulp.value(problema.objective))
