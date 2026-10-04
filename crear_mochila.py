from random import randint


def crear_mochila(n):
    nombre="mochila"+str(n)+".txt"
    arch=open(nombre,"w")
    cap=n*50
    arch.write(str(cap)+"\n")
    for i in range (n):
        peso=randint(1,200);
        benef=randint(1,1000);
        arch.write(str(peso)+","+str(benef)+"\n")
    arch.close()


crear_mochila(1000)

# Esta función crea una mochila con una lista del tamaño indicado como parámetro
# Los beneficios están en el rango 1-1000
# Los pesos están en el rango 1-200
# La capacidad de la mochila es tamaño * 50: aprox, la mitad de los elementos cabrán en la mochila
#
# Se genera un archivo cuya primera línea es la capacidad de la mochila
# Las líneas siguientes son pares ordenados (peso, beneficio) de cada elemento.


def reed(archivo):
    texto = open(archivo,"r")
    capacidad = int(texto.readline())

    objetos = []
    for linea in texto:
        peso, beneficio = linea.strip().split(',')
        objetos.append((int(peso), int(beneficio)))

    texto.close()
    return objetos, capacidad


# =============================================================================
# PROBLEMA 1: FUERZA BRUTA
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
# PROBLEMA 1: BACKTRACKING (PODA POR FACTIBILIDAD Y COTA SUPERIOR)
# =============================================================================
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


# ============================================================================
# PROBLEMA 2: GREEDY
# ==============================================================================
def greedy(objetos, capacidad):
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

    return result


objetos, capacidad = reed("mochila1000.txt")
solucion = greedy(objetos, capacidad)