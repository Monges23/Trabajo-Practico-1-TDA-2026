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
