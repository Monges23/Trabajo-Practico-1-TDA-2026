"""Instancia de mochila 0/1 y su formato de archivo.

Formato, heredado del TP1 (`crear_mochila.py`), que es el que usan todos los
sets de datos del repositorio:

    linea 1        : capacidad W de la mochila
    lineas 2..n+1  : "peso,beneficio" de cada elemento

En el TP1 el parseo devolvia la tupla `(v, p, n, w)` -- valores primero, pesos
despues -- mientras que el generador escribia "peso,beneficio". Con listas
sueltas ese orden invertido produce errores silenciosos (nadie nota que paso
beneficios donde iban pesos hasta que el resultado es absurdo). Por eso aca la
instancia es un objeto con campos con nombre.

El archivo se lee y se escribe en el mismo formato, sin columnas extra, para
que los sets del TP1 sigan siendo validos y para que P4 compare sobre las
mismas instancias.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Instancia:
    """Mochila 0/1: el elemento `i` aporta `beneficios[i]` y cuesta `pesos[i]`."""

    pesos: list[int]
    beneficios: list[int]
    capacidad: int
    nombre: str = ""

    def __post_init__(self) -> None:
        if len(self.pesos) != len(self.beneficios):
            raise ValueError(
                f"pesos y beneficios tienen distinto largo: "
                f"{len(self.pesos)} != {len(self.beneficios)}"
            )
        if not self.pesos:
            raise ValueError("la instancia no tiene elementos")
        if self.capacidad <= 0:
            raise ValueError(f"capacidad invalida: {self.capacidad}")
        for i, peso in enumerate(self.pesos):
            if peso <= 0:
                raise ValueError(f"peso no positivo en el elemento {i}: {peso}")
        for i, beneficio in enumerate(self.beneficios):
            if beneficio < 0:
                raise ValueError(f"beneficio negativo en el elemento {i}: {beneficio}")

    @property
    def n(self) -> int:
        """Cantidad de elementos."""
        return len(self.pesos)

    def __len__(self) -> int:
        return len(self.pesos)

    def peso_de(self, seleccion) -> int:
        """Peso total de una seleccion de indices."""
        return sum(self.pesos[i] for i in seleccion)

    def beneficio_de(self, seleccion) -> int:
        """Beneficio total de una seleccion de indices."""
        return sum(self.beneficios[i] for i in seleccion)

    def peso_total(self) -> int:
        """Peso si se tomaran todos los elementos."""
        return sum(self.pesos)

    def beneficio_total(self) -> int:
        """Beneficio de tomar todos los elementos: techo trivial de cualquier solucion."""
        return sum(self.beneficios)

    def descripcion(self) -> str:
        return (
            f"{self.nombre or '<sin nombre>'}: n={self.n} W={self.capacidad} "
            f"peso_total={self.peso_total()} beneficio_total={self.beneficio_total()}"
        )


def leer(ruta: str | Path) -> Instancia:
    """Lee una instancia del formato del TP1."""
    ruta = Path(ruta)
    with ruta.open("r", encoding="utf-8") as arch:
        lineas = [(n, linea.strip()) for n, linea in enumerate(arch, start=1)]
    lineas = [(n, linea) for n, linea in lineas if linea]
    if not lineas:
        raise ValueError(f"{ruta}: archivo vacio")

    numero, primera = lineas[0]
    try:
        capacidad = int(primera)
    except ValueError:
        raise ValueError(
            f"{ruta}:{numero}: la primera linea debe ser la capacidad, no {primera!r}"
        ) from None

    pesos: list[int] = []
    beneficios: list[int] = []
    for numero, linea in lineas[1:]:
        partes = linea.split(",")
        if len(partes) != 2:
            raise ValueError(f"{ruta}:{numero}: se esperaba 'peso,beneficio', no {linea!r}")
        try:
            peso, beneficio = int(partes[0]), int(partes[1])
        except ValueError:
            raise ValueError(f"{ruta}:{numero}: valores no enteros en {linea!r}") from None
        pesos.append(peso)
        beneficios.append(beneficio)

    return Instancia(pesos, beneficios, capacidad, nombre=ruta.name)


def escribir(inst: Instancia, ruta: str | Path) -> None:
    """Escribe una instancia en el formato del TP1."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8") as arch:
        arch.write(f"{inst.capacidad}\n")
        for peso, beneficio in zip(inst.pesos, inst.beneficios):
            arch.write(f"{peso},{beneficio}\n")
