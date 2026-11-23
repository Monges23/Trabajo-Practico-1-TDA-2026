"""Medicion de tiempo y memoria, portada de `tp1/complejidad/util.py`.

POR QUE SE REHACE EN VEZ DE REUTILIZAR LOS CSV DEL TP1
El arnes del TP1 tenia dos problemas para P4:

1. Medía con `ProcessPoolExecutor` (varios procesos en paralelo). Los tiempos
   quedan contaminados por contencion de CPU y por el escalado de frecuencia, y
   los numeros dependen de cuantos nucleos habia libres. Forma de medir: la de
   aca es secuencial.
2. Medía con `time.time()`, que es el reloj de pared y puede saltar (NTP). Aca
   se usa `time.perf_counter()`, monotono y de mayor resolucion.

Consecuencia: para P4 hay que re-medir los algoritmos del TP1 con este mismo
arnes. Comparar los tiempos nuevos contra `tp1/complejidad/tiempos_*.csv` mide
la diferencia entre dos metodos de medicion, no entre dos algoritmos.

Ademas del promedio se guardan los tiempos crudos, el desvio y la mediana: con
diez corridas el promedio solo no dice nada sobre la dispersion, y el informe
pide analizar si la curva medida sigue a la teorica.
"""

from __future__ import annotations

import statistics
import time
import tracemalloc
from dataclasses import dataclass, field

# Cuantas veces se ejecuta cada tamano. Se promedian para reducir el error
# estadistico, igual que en el TP1.
RUNS_POR_TAMANO = 10


@dataclass
class Resumen:
    """Resultado de medir una funcion varias veces."""

    estado: str = "ok"  # ok | error
    tiempos: list[float] = field(default_factory=list)
    error: str | None = None

    @property
    def media(self) -> float:
        return statistics.fmean(self.tiempos) if self.tiempos else float("nan")

    @property
    def mediana(self) -> float:
        return statistics.median(self.tiempos) if self.tiempos else float("nan")

    @property
    def desvio(self) -> float:
        return statistics.stdev(self.tiempos) if len(self.tiempos) > 1 else 0.0

    @property
    def minimo(self) -> float:
        return min(self.tiempos) if self.tiempos else float("nan")

    def __str__(self) -> str:
        if self.estado != "ok":
            return f"error: {self.error}"
        return (
            f"media={self.media:.6f}s mediana={self.mediana:.6f}s "
            f"min={self.minimo:.6f}s desvio={self.desvio:.6f}s ({len(self.tiempos)} corridas)"
        )


def medir(funcion, *args, repeticiones: int = RUNS_POR_TAMANO, **kwargs) -> Resumen:
    """Ejecuta `funcion(*args, **kwargs)` `repeticiones` veces y mide el tiempo."""
    resumen = Resumen()
    try:
        for _ in range(repeticiones):
            inicio = time.perf_counter()
            funcion(*args, **kwargs)
            resumen.tiempos.append(time.perf_counter() - inicio)
    except Exception as exc:  # se reporta como celda fallida, no rompe la corrida
        resumen.estado = "error"
        resumen.error = f"{type(exc).__name__}: {exc}"
    return resumen


def medir_por_tamanos(funcion, tamanos, obtener_args, repeticiones: int = RUNS_POR_TAMANO):
    """Mide `funcion(*obtener_args(n))` para cada tamano. Devuelve {n: Resumen}."""
    return {
        n: medir(funcion, *obtener_args(n), repeticiones=repeticiones) for n in tamanos
    }


def medir_memoria(funcion, *args, **kwargs) -> int:
    """Pico de memoria (bytes) de una ejecucion, medido con tracemalloc.

    Lo necesita P3, que debe justificar el orden de complejidad espacial.
    No incluye lo que asigna librerias de C (tracemalloc solo ve las
    asignaciones de Python).
    """
    tracemalloc.start()
    try:
        funcion(*args, **kwargs)
        _, pico = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return pico
