from random import randint
import os
import random
import sys
import time
BASE = os.path.dirname(os.path.abspath(__file__))
DIR_SETS = os.path.join(BASE, "sets_datos")

import pulp



def leer_mochila(nombre):
    """Devuelve (capacidad, pesos, beneficios). O(n)."""
    with open(nombre) as f:
        cap = int(f.readline())
        pesos, benef = [], []
        for linea in f:
            linea = linea.strip()
            if linea:
                p, b = linea.split(",")
                pesos.append(int(p))
                benef.append(int(b))
    return cap, pesos, benef


def resolver_mochila(cap, pesos, benef):
    """Resuelve la mochila 0/1 con PuLP (solver CBC).

    Devuelve (beneficio_optimo, seleccion, t_modelo, t_solver)."""
    n = len(pesos)
    t0 = time.perf_counter()
    prob = pulp.LpProblem("Mochila", pulp.LpMaximize)
    Y = pulp.LpVariable.dicts("Y", range(n), cat="Binary")
    prob += pulp.lpSum(benef[i] * Y[i] for i in range(n))             
    prob += pulp.lpSum(pesos[i] * Y[i] for i in range(n)) <= cap     
    t1 = time.perf_counter()
    prob.solve(pulp.PULP_CBC_CMD(msg=0))                             
    t2 = time.perf_counter()
    seleccion = [i for i in range(n) if Y[i].value() is not None and Y[i].value() > 0.5]
    total = sum(benef[i] for i in seleccion)
    return total, seleccion, t1 - t0, t2 - t1


if __name__ == "__main__":
    nombre = sys.argv[1] if len(sys.argv) > 1 else os.path.join(DIR_SETS, "mochila1000.txt")
    cap, pesos, benef = leer_mochila(nombre)
    total, sel, tm, ts = resolver_mochila(cap, pesos, benef)
    print("Archivo: %s" % nombre)
    print("Capacidad: %d  Elementos: %d" % (cap, len(pesos)))
    print("Beneficio optimo: %d" % total)
    print("Peso usado: %d  Elementos elegidos: %d" % (sum(pesos[i] for i in sel), len(sel)))
    print("Tiempo armado del modelo: %.4f s   Tiempo solver: %.4f s" % (tm, ts))
    print("Indices elegidos:", sel)