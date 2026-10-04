from random import randint, seed

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



def generar_instancia(n_elementos, capacidad_proporcion=0.5, peso_min=1, peso_max=50, valor_min=10, valor_max=100, seed=None):
    """
    Genera pesos, valores y capacidad para el problema de la mochila 0/1.
    """
    if seed is not None:
        seed(seed)
    
    pesos = [randint(peso_min, peso_max) for _ in range(n_elementos)]
    valores = [randint(valor_min, valor_max) for _ in range(n_elementos)]
    capacidad = int(sum(pesos) * capacidad_proporcion)
    
    return pesos, valores, capacidad

if __name__ == "__main__":
    p, v, c = generar_instancia(10, seed=42)
    print("Capacidad:", c)
    print("Pesos:", p)
    print("Valores:", v)
