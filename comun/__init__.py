"""Codigo compartido del TP2: instancias, solvers y medicion.

Esta carpeta se completa en la rama base y despues queda congelada: las ramas
p1, p2, p3 y p4 la usan pero no la editan. Si un punto necesita algo nuevo, se
agrega un archivo nuevo (nunca se reescribe el de otro).

Las instancias son archivos planos (`comun/crear_mochila.py`) y se leen con
`comun/parser_mochila.py`, que devuelve `(elems, n, w)` con `elems[i]` el par
`(peso, beneficio)`. Ese trio es el contrato de todos los solvers de `comun` y
todos devuelven `(valor, seleccion)`.

Convencion de imports: los archivos de adentro de `comun` usan imports
relativos (`from .parser_mochila import parsear_mochila`). Los scripts de cada
punto arrancan con este bootstrap para que `comun` sea importable desde
cualquier directorio:

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

    from comun.parser_mochila import parsear_mochila
    from comun.exacto import dinamica
"""
