"""Resultado uniforme de cualquier solver de mochila.

En el TP1 cada metodo devolvia una cosa distinta: fuerza bruta un entero,
greedy una lista de objetos, programacion lineal una tupla de cuatro valores
(beneficio, seleccion, tiempo de armado, tiempo de solver). Para comparar en P4
y para verificar factibilidad en P1 hace falta una sola forma de respuesta.

`valor` es `float` solo en la relajacion lineal, donde el optimo puede ser
fraccionario; para cualquier solver entero es un `int`.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Solucion:
    """Valor obtenido, indices elegidos y (opcional) traza del seguimiento."""

    valor: float
    seleccion: list[int] = field(default_factory=list)
    traza: list[str] | None = field(default=None, repr=False)

    def peso(self, inst) -> int:
        return inst.peso_de(self.seleccion)

    def es_factible(self, inst) -> bool:
        return (
            len(set(self.seleccion)) == len(self.seleccion)
            and all(0 <= i < inst.n for i in self.seleccion)
            and inst.peso_de(self.seleccion) <= inst.capacidad
        )

    def verificar(self, inst) -> None:
        """Lanza ValueError si la solucion no es factible o el valor no coincide."""
        if not self.es_factible(inst):
            raise ValueError(
                f"solucion no factible: peso={self.peso(inst)} > W={inst.capacidad} "
                f"o indices invalidos/repetidos {self.seleccion[:10]}"
            )
        real = inst.beneficio_de(self.seleccion)
        if int(self.valor) != real:
            raise ValueError(
                f"valor declarado {self.valor} != beneficio de la seleccion {real}"
            )

    def __str__(self) -> str:
        return f"valor={self.valor} elementos={len(self.seleccion)}"
