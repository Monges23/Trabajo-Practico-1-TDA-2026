"""Solvers exactos del TP1, portados a un API comun.

Todos comparten el contrato de datos de `comun/parser_mochila.py`:
`elems[i]` es el par `(peso, beneficio)`, `n` la cantidad de elementos y `w` la
capacidad. Todos devuelven `(valor, seleccion)`, o sea que se pueden encadenar
directo con el parser:

    elems, n, w = parsear_mochila("mochila1500.txt")
    valor, seleccion = dinamica.resolver(elems, n, w)

El TP1 devolvia solo el valor en fuerza bruta, backtracking y programacion
dinamica, asi que hubo que agregar la reconstruccion de la seleccion: sin ella
no se puede verificar factibilidad ni calcular cotas sobre el resultado.

Uso previsto:
- P1: `programacion_lineal` da el optimo exacto (decision del grupo: PL como
  metodo de solucion optima) y `programacion_lineal.relajacion` la cota.
- P2 y P3: el optimo de referencia para medir la brecha del aproximado.
- P4: las curvas de FB, BT y PD del TP1.

Recordar que FB y BT son exponenciales: solo sirven para instancias chicas
(el TP1 llego a n=24) y la recursion de Python se corta cerca de n=1000.
"""

from . import backtracking, dinamica, fuerza_bruta, programacion_lineal

__all__ = ["backtracking", "dinamica", "fuerza_bruta", "programacion_lineal"]
