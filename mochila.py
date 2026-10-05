import pulp

import time
import sys
import os


def reed(archivo):
    texto = open(archivo,"r")
    capacidad = int(texto.readline())

    objetos = []
    for linea in texto:
        peso, beneficio = linea.strip().split(',')
        objetos.append((int(peso), int(beneficio)))

    texto.close()
    return objetos, capacidad

# ==============================================================================
# PROBLEMA 1.1: FUERZA BRUTA
# ==============================================================================
def mochila_fuerza_bruta(objetos, capacidad):
    n = len(objetos)

    def resolver(indice, peso_actual, beneficio_actual):
        if indice == n:
            if peso_actual <= capacidad:
                return beneficio_actual
            return 0
        beneficio_sin = resolver(indice + 1, peso_actual, beneficio_actual)
        beneficio_con = resolver(
            indice + 1,
            peso_actual + objetos[indice][0],
            beneficio_actual + objetos[indice][1],
        )

        return max(beneficio_sin, beneficio_con)

    return resolver(0, 0, 0)

# ==============================================================================
# PROBLEMA 1.2: BACKTRACKING (PODA POR FACTIBILIDAD Y COTA SUPERIOR)
# ==============================================================================
def mochila_backtracking(objetos, capacidad):

    n = len(objetos)

    sufijo_beneficios = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        sufijo_beneficios[i] = sufijo_beneficios[i + 1] + objetos[i][1]
    mejor_beneficio = 0
    def resolver(indice, peso_actual, beneficio_actual):
        nonlocal mejor_beneficio
        if beneficio_actual > mejor_beneficio:
            mejor_beneficio = beneficio_actual
        if indice == n:
            return
        if beneficio_actual + sufijo_beneficios[indice] <= mejor_beneficio:
            return
        peso_item, benef_item = objetos[indice]
        if peso_actual + peso_item <= capacidad:
            resolver(
                indice + 1, peso_actual + peso_item, beneficio_actual + benef_item
            )
        resolver(indice + 1, peso_actual, beneficio_actual)

    resolver(0, 0, 0)
    return mejor_beneficio

# ==============================================================================
# PROBLEMA 2: GREEDY
# ==============================================================================
def mochila_greedy(objetos, capacidad):
    result = []
    peso_contador = 0
    beneficio_total = 0

    objetos.sort(key=lambda x: x[1] / x[0], reverse=True)

    elemento_critico = None

    for objeto in objetos:
        peso, beneficio = objeto

        if peso_contador + peso <= capacidad:
            peso_contador += peso
            beneficio_total += beneficio
            result.append(objeto)
        else:
            elemento_critico = objeto
            break

    if elemento_critico is not None:
        beneficio_critico = elemento_critico[1]
        if beneficio_critico > beneficio_total:
            result = [elemento_critico]
            beneficio_total = beneficio_critico

    return result, beneficio_total

# ==============================================================================
# PROBLEMA 3: PROGRAMACION DINAMICA (OG y ALT)
# ==============================================================================
def parsear_mochila(archivo: str) -> tuple[list[int], list[int], int, int]:
    with open(archivo, "r", encoding="utf-8") as arch:
        lineas = [linea.strip() for linea in arch if linea.strip()]

    w = int(lineas[0])

    p: list[int] = []
    v: list[int] = []
    for i, linea in enumerate(lineas[1:], start=2):
        partes = linea.split(",")
        p.append(int(partes[0]))
        v.append(int(partes[1]))

    n = len(p)
    return v, p, n, w

def mochila_pd(valores: list[int], pesos:list[int], cant_elems: int, capacidad_mochila: int):
    memo: list[list[int]] = []
    for i in range(cant_elems + 1):
        memo.append([0] * (capacidad_mochila + 1))

    for elem in range(1, cant_elems + 1):
        valor_actual: int = valores[elem - 1]
        peso_actual: int = pesos[elem - 1]

        for w in range(1, capacidad_mochila + 1):
            if (peso_actual <= w):
                memo[elem][w] = max((valor_actual + memo[elem-1][w-peso_actual]), memo[elem-1][w])
            else:
                memo[elem][w] = memo[elem-1][w]

    return memo[cant_elems][capacidad_mochila]

def mochila_pd_alt(valores: list[int], pesos:list[int], cant_elems: int, beneficio: int):
    inf = float('inf')

    memo = []
    for i in range(cant_elems + 1):
        # no inicializamos en 0, pues estamos buscando el minimo.
        # al tener nuestros valores >= 1, nunca obtendremos algo < 0
        # por ende el 0 siempre ganaria en nuestra eq de recurrencia
        memo.append([inf] * (beneficio + 1))

    for i in range(cant_elems + 1):
        # conseguir beneficio 0 cuesta 0
        memo[i][0] = 0

    for elem in range(1, cant_elems + 1):
        valor_actual: int = valores[elem - 1]
        peso_actual: int = pesos[elem - 1]

        for b in range(1, beneficio + 1):
            # usamos max(0, b-valor_actual) pues queremos al menos B de beneficio
            # si valor actual > B entonces al restarlo obtendriamos un indice negativo
            # lo que romperia el codigo y el problema
            memo[elem][b] = min((peso_actual + memo[elem-1][max(0, b-valor_actual)]), memo[elem-1][b])

    return memo[cant_elems][beneficio]

# ==============================================================================
# PROBLEMA 4: PROGRAMACION LINEAL
# ==============================================================================
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

def mochila_pl(cap, pesos, benef):
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


def show_menu():
    print("\n--- Elegir Estrategia Para Resolver Mochila ---")
    print("1. Fuerza Bruta")
    print("2. BackTracking")
    print("3. Greedy")
    print("4. Programacion Dinamica (Og)")
    print("5. Programacion Dinamica (Alt)")
    print("6. Programacion Lineal")
    print("7. Exit")

def main():
    while True:
        show_menu()
        choice = input("Elegir opcion (1-7): ").strip()

        if choice == "1":
            print("Resolviendo mochila mediante fuerza bruta")
            obj, cap = reed("mochila.txt")
            res = mochila_fuerza_bruta(obj, cap)
            print("Beneficio optimo: ", res)
        elif choice == "2":
            print("Resolviendo mochila mediante backtracking")
            obj, cap = reed("mochila.txt")
            res = mochila_backtracking(obj, cap)
            print("Beneficio optimo: ", res)
        elif choice == "3":
            print("Resolviendo mochila mediante greedy")
            obj, cap = reed("mochila.txt")
            res, beneficio = mochila_greedy(obj, cap)
            print("Beneficio optimo: ", beneficio)
        elif choice == "4":
            print("Resolviendo mochila ORIGINAL mediante programacion dinamica")
            v,p,n,w = parsear_mochila("mochila.txt")
            res = mochila_pd(v,p,n,w)
            print("Beneficio optimo: ", res)
        elif choice == "5":
            print("Resolviendo mochila ALTERNATIVO mediante programacion dinamica")
            v,p,n,w = parsear_mochila("mochila.txt")
            res = mochila_pd_alt(v,p,n,w)
            print("Peso minimo: ", res)
        elif choice == "6":
            print("Resolviendo mochila mediante programacion lineal")
            cap, pesos, benef = leer_mochila("mochila.txt")
            res = mochila_pl(cap, pesos, benef)
            print("Beneficio optimo: ", res[0])
        elif choice == "7":
            print("Saliendo")
            break
        else:
            print("Opcion Invalida. Por favor seleccione una opcion entre 1-7")

if __name__ == "__main__":
    main()
