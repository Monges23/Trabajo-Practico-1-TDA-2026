"""Genera los sets de datos de las cuatro familias en `datos/`
"""

import os
import pathlib
import random
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from comun.crear_mochila import crear_mochila

SEMILLA = 2026
TAMANOS = [10, 20, 40, 80, 120, 160]
DATOS = RAIZ / "datos"

def escribir(ruta: pathlib.Path, capacidad: int, elems) -> None:
    with open(ruta, "w", encoding="utf-8") as arch:
        arch.write(f"{capacidad}\n")
        for peso, beneficio in elems:
            arch.write(f"{peso},{beneficio}\n")


def beneficio_familia(familia: str, peso: int, rng: random.Random) -> int:
    if familia == "debilmente-correlacionadas":
        return max(1, peso + rng.randint(-20, 20))
    if familia == "fuertemente-correlacionadas":
        return peso + 20
    if familia == "subset-sum":
        return peso
    raise ValueError(familia)


def main(tamaños):
    carpeta = DATOS / "uncorrelacionadas"
    carpeta.mkdir(parents=True, exist_ok=True)
    random.seed(SEMILLA)
    actual = os.getcwd()
    os.chdir(carpeta)
    try:
        for n in tamaños:
            crear_mochila(n)
    finally:
        os.chdir(actual)
 
    for familia in ("debilmente-correlacionadas", "fuertemente-correlacionadas", "subset-sum"):
        carpeta = DATOS / familia
        carpeta.mkdir(parents=True, exist_ok=True)
        rng = random.Random(SEMILLA)
        for n in tamaños:
            elems = []
            for _ in range(n):
                peso = rng.randint(1, 200)
                elems.append((peso, beneficio_familia(familia, peso, rng)))
            escribir(carpeta / f"mochila{n}.txt", n * 50, elems)
    print("Instancias generadas en", DATOS)


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]] or TAMANOS)