# el codigo fue modificaco para simplificar la vida del corrector

import sys
from random import randint

def crear_mochila(n):
    nombre="mochila.txt"
    arch=open(nombre,"w")
    cap=n*50
    arch.write(str(cap)+"\n")
    for i in range (n):
        peso=randint(1,200);
        benef=randint(1,1000);
        arch.write(str(peso)+","+str(benef)+"\n")
    arch.close()

# Esta función crea una mochila con una lista del tamaño indicado como parámetro
# Los beneficios están en el rango 1-1000
# Los pesos están en el rango 1-200
# La capacidad de la mochila es tamaño * 50: aprox, la mitad de los elementos cabrán en la mochila
#
# Se genera un archivo cuya primera línea es la capacidad de la mochila
# Las líneas siguientes son pares ordenados (peso, beneficio) de cada elemento.

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Pasar como argumento el N deseado")
    n = sys.argv[1]
    crear_mochila(int(n))
