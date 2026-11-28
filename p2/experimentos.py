"""Experimentos del P2: corre el FPTAS sobre los sets de `datos/` con varios epsilon,
guarda `p2/resultados/resultados_p2.csv` y genera los graficos (curva medida + curva teorica).
"""

import argparse
import csv
import pathlib
import statistics
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
 
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  
import numpy as np  

from comun.exacto import dinamica  
from comun.parser_mochila import parsear_mochila 
from p2.mochila import resolver  

FAMILIAS = {  
    "uncorrelacionadas": "no correlacionada",
    "debilmente-correlacionadas": "débilmente correlacionada",
    "fuertemente-correlacionadas": "fuertemente correlacionada",
    "subset-sum": "subset-sum",
}

EPSILONS = [1, 1 / 2, 1 / 5, 1 / 10, 1 / 20]
SALIDA = RAIZ / "p2" / "resultados"
LIMITE_UNA_CORRIDA = 2.0

def medir(funcion, reps):
    inicio = time.perf_counter()
    resultado = funcion()
    tiempos = [time.perf_counter() - inicio]
    if tiempos[0] <= LIMITE_UNA_CORRIDA:
        for _ in range(reps - 1):
            inicio = time.perf_counter()
            funcion()
            tiempos.append(time.perf_counter() - inicio)
    return resultado, statistics.median(tiempos)
 
 
def ajuste_origen(x, y):
    """Cuadrados minimos de y = a*x (a > 0)."""
    x, y = np.array(x, float), np.array(y, float)
    return float(x @ y / (x @ x))

def correr(n_max, reps):
    filas = []
    for carpeta, nombre in FAMILIAS.items():
        archivos = sorted(
            (RAIZ / "datos" / carpeta).glob("mochila*.txt"),
            key=lambda ruta: int(ruta.stem.removeprefix("mochila")),
        )
        for ruta in archivos:
            elems, n, w = parsear_mochila(str(ruta))
            if n_max and n > n_max:
                continue
            optimo, t_exacta = medir(lambda: dinamica.valor_compacto(elems, n, w), reps)
            for eps in EPSILONS:
                (valor, seleccion), t = medir(lambda: resolver(elems, n, w, eps), reps)
                inv = round(1 / eps)
                fila = dict(
                    familia=carpeta, n=n, W=w, epsilon=eps, inv_eps=inv, resultado=valor,
                    optimo=optimo, cociente=round(valor / optimo, 5),
                    cumple_cota=valor >= (1 - eps) * optimo,
                    tiempo_fptas_s=round(t, 6), tiempo_exacta_s=round(t_exacta, 6),
                )
                filas.append(fila)
                print(
                    f"{carpeta:28s} n={n:4d} eps=1/{inv:<3d} FPTAS={valor:7d} OPT={optimo:7d} "
                    f"({fila['cociente']:.4f}) t={t:8.4f}s cota={'OK' if fila['cumple_cota'] else 'FALLA'}",
                    flush=True,
                )
    return filas


def graficar(filas):
    colores = dict(zip(FAMILIAS, ["tab:blue", "tab:orange", "tab:green", "tab:red"]))
    n_fijo = max(f["n"] for f in filas)
 
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
    for carpeta, nombre in FAMILIAS.items():
        pts = sorted((f["n"], f["tiempo_fptas_s"]) for f in filas
                     if f["familia"] == carpeta and f["inv_eps"] == 10)
        xs, ys = zip(*pts)
        a = ajuste_origen([x**3 for x in xs], ys)
        xx = np.linspace(min(xs), max(xs), 100)
        ax[0].plot(xs, ys, "o-", color=colores[carpeta], label=f"medido: {nombre}")
        ax[0].plot(xx, a * xx**3, "--", color=colores[carpeta], alpha=0.7, lw=1)
        print(f"ajuste a*n^3 (eps=1/10) {carpeta}: a={a:.3e}")
    ax[0].plot([], [], "k--", lw=1, label="ajuste a·n³ (por familia)")
    ax[0].set_xlabel("n (cantidad de elementos)")
    ax[0].set_ylabel("Tiempo [s]")
    ax[0].set_title("Tiempo vs n  (ε = 1/10)")
    ax[0].legend(fontsize=7)
    ax[0].grid(alpha=0.3)
 
    for carpeta, nombre in FAMILIAS.items():
        pts = sorted((f["inv_eps"], f["tiempo_fptas_s"]) for f in filas
                     if f["familia"] == carpeta and f["n"] == n_fijo)
        xs, ys = zip(*pts)
        a = ajuste_origen(xs, ys)
        xx = np.linspace(min(xs), max(xs), 100)
        ax[1].plot(xs, ys, "o-", color=colores[carpeta], label=f"medido: {nombre}")
        ax[1].plot(xx, a * xx, "--", color=colores[carpeta], alpha=0.7, lw=1)
        print(f"ajuste a*(1/eps) (n={n_fijo}) {carpeta}: a={a:.3e}")
    ax[1].plot([], [], "k--", lw=1, label="ajuste a·(1/ε) (por familia)")
    ax[1].set_xlabel("1/ε")
    ax[1].set_ylabel("Tiempo [s]")
    ax[1].set_title(f"Tiempo vs 1/ε  (n = {n_fijo})")
    ax[1].legend(fontsize=7)
    ax[1].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(SALIDA / "grafico_tiempos_p2.png", dpi=150)
    plt.close(fig)
 
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
    marcadores = dict(zip(FAMILIAS, ["o", "s", "^", "D"]))
    for eje in ax:
        for carpeta, nombre in FAMILIAS.items():
            pts = [(f["epsilon"], f["cociente"]) for f in filas if f["familia"] == carpeta]
            eje.scatter(*zip(*pts), marker=marcadores[carpeta], color=colores[carpeta],
                        label=nombre, alpha=0.7)
        eje.set_xlabel("ε")
        eje.set_ylabel("resultado / óptimo")
        eje.grid(alpha=0.3)
    ee = np.linspace(0.05, 1, 100)
    ax[0].plot(ee, 1 - ee, "k--", label="cota garantizada 1 − ε")
    ax[0].set_ylim(0, 1.05)
    ax[0].set_title("Calidad de la solución")
    ax[0].legend(fontsize=7)
    ax[1].set_ylim(0.975, 1.003)
    ax[1].set_title("Detalle (zoom cerca de 1)")
    fig.tight_layout()
    fig.savefig(SALIDA / "grafico_calidad_p2.png", dpi=150)
    plt.close(fig)


def leer_csv():
    with open(SALIDA / "resultados_p2.csv", encoding="utf-8") as arch:
        filas = list(csv.DictReader(arch))
    for f in filas:
        for clave in ("n", "W", "inv_eps", "resultado", "optimo"):
            f[clave] = int(f[clave])
        for clave in ("epsilon", "cociente", "tiempo_fptas_s", "tiempo_exacta_s"):
            f[clave] = float(f[clave])
    return filas


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-max", type=int, default=None, help="no correr instancias con n mayor")
    parser.add_argument("--reps", type=int, default=3, help="repeticiones por medicion (mediana)")
    parser.add_argument("--solo-graficos", action="store_true",
                        help="regenerar los graficos desde resultados_p2.csv sin volver a correr")
    args = parser.parse_args()
 
    SALIDA.mkdir(parents=True, exist_ok=True)
    if args.solo_graficos:
        graficar(leer_csv())
        sys.exit(0)
    filas = correr(args.n_max, args.reps)
    with open(SALIDA / "resultados_p2.csv", "w", newline="", encoding="utf-8") as arch:
        escritor = csv.DictWriter(arch, fieldnames=filas[0].keys())
        escritor.writeheader()
        escritor.writerows(filas)
    graficar(filas)
    print("\nCota (1 - eps) cumplida en todas las ejecuciones:", all(f["cumple_cota"] for f in filas))