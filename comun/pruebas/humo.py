"""Verificacion de humo de `comun`: que los solvers coincidan entre si.

Se corre con `python3 comun/pruebas/humo.py` desde cualquier directorio. No usa
pytest a proposito: el zip de entrega tiene que correr con lo que haya, y una
dependencia menos es una cosa menos que puede fallar en la maquina del corrector.

Que se verifica (son las invariantes que sostienen P1, P2 y P4):

1. Fuerza bruta, backtracking y las dos PD dan el mismo optimo.
2. Greedy (Sahni) devuelve una solucion factible y z*/2 <= valor <= z*.
3. La relajacion lineal es cota superior del optimo y el optimo entero de PL
   coincide con la fuerza bruta (si PuLP esta instalado; si no, se avisa y se
   sigue: las ramas de P2 y P3 no dependen de PuLP).
4. Ida y vuelta del formato de archivo de instancias.
"""

from __future__ import annotations

import math
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from comun.exacto import backtracking, dinamica, fuerza_bruta, programacion_lineal
from comun.generar import generar
from comun.greedy import greedy
from comun.instancia import Instancia, leer, escribir


def main() -> int:
    fallas: list[str] = []

    def check(condicion: bool, mensaje: str) -> None:
        if condicion:
            print(f"  ok   {mensaje}")
        else:
            print(f"  FALLA {mensaje}")
            fallas.append(mensaje)

    inst = generar(14, semilla=1)
    print(f"instancia de prueba: {inst.descripcion()}")

    print("\n1. exactos coinciden")
    fb = fuerza_bruta.resolver(inst)
    bt = backtracking.resolver(inst)
    dp = dinamica.resolver(inst)
    dpc = dinamica.valor_compacto(inst)
    optimo = fb.valor
    for nombre, solucion in (("backtracking", bt), ("dinamica", dp)):
        check(solucion.valor == optimo, f"{nombre} = {solucion.valor} (fb = {optimo})")
        check(solucion.es_factible(inst), f"{nombre} devuelve una seleccion factible")
        solucion.verificar(inst)
    check(dpc == optimo, f"dinamica compacta = {dpc}")

    print("\n2. greedy / Sahni")
    sol = greedy(inst)
    check(sol.es_factible(inst), f"greedy factible (peso {sol.peso(inst)} <= {inst.capacidad})")
    check(
        optimo / 2 <= sol.valor <= optimo,
        f"optimo/2 = {optimo / 2} <= greedy = {sol.valor} <= optimo = {optimo}",
    )

    print("\n3. programacion lineal")
    try:
        pl = programacion_lineal.resolver(inst)
        cota = programacion_lineal.relajacion(inst)
        check(pl.valor == optimo, f"PL entero = {pl.valor} = optimo")
        check(pl.es_factible(inst), "PL devuelve una seleccion factible")
        check(
            cota >= optimo - 1e-6,
            f"relajacion {cota:.4f} >= optimo {optimo}",
        )
        check(
            math.floor(cota) >= optimo,
            f"floor(relajacion) = {math.floor(cota)} es cota entera valida",
        )
        # Cota ajustada: la relajacion solo difiere del optimo en el elemento
        # critico fraccionario, asi que la brecha no puede superar el beneficio
        # mas grande. Sin esta verificacion, una relajacion sin x <= 1 daba
        # 35247 contra un optimo de 5593 y "pasaba" por ser >= optimo.
        check(
            cota - optimo <= max(inst.beneficios) + 1e-6,
            f"brecha de relajacion {cota - optimo:.2f} <= max beneficio {max(inst.beneficios)}",
        )
        check(
            cota <= inst.beneficio_total() + 1e-6,
            f"relajacion {cota:.2f} <= suma de beneficios {inst.beneficio_total()}",
        )
    except ModuleNotFoundError as exc:
        print(f"  omite  {exc}")

    print("\n4. casos borde del greedy")
    # El TP1 devolvia el elemento critico aunque no entrara solo en la mochila y
    # la solucion quedaba infactible. Estos tres casos lo fijan.
    bordes = {
        "ningun elemento entra": Instancia([10, 10, 10], [5, 5, 5], 5, "nada-entra"),
        "un elemento pesa mas que W": Instancia([10, 1], [1, 100], 10, "critico-no-entra"),
        "empate prefijo vs critico": Instancia([10, 7], [70, 70], 10, "empate"),
    }
    for etiqueta, borde in bordes.items():
        sol_borde = greedy(borde)
        check(
            sol_borde.es_factible(borde),
            f"{etiqueta}: greedy factible (peso {sol_borde.peso(borde)} <= {borde.capacidad})",
        )
        check(
            fuerza_bruta.resolver(borde).valor == dinamica.resolver(borde).valor,
            f"{etiqueta}: exactos coinciden",
        )

    print("\n5. formato de archivo")
    with tempfile.TemporaryDirectory() as tmp:
        ruta = pathlib.Path(tmp) / "mochila14.txt"
        escribir(inst, ruta)
        releida = leer(ruta)
        check(
            (releida.pesos, releida.beneficios, releida.capacidad)
            == (inst.pesos, inst.beneficios, inst.capacidad),
            "ida y vuelta del formato conserva pesos, beneficios y capacidad",
        )

    print(f"\n{'FALLARON' if fallas else 'TODO OK'}: {len(fallas)} fallas")
    return 1 if fallas else 0


if __name__ == "__main__":
    raise SystemExit(main())
