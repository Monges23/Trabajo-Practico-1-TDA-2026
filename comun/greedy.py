"""Greedy del TP1 (Ej 2), que es tambien el algoritmo de Sahni (1975).

Algoritmo: ordenar por beneficio/peso descendente, llenar mientras entre
(prefijo greedy), y si hay un elemento critico que no entra, comparar el
beneficio del prefijo contra el beneficio de ese elemento solo. Se devuelve el
mejor de los dos.

Esa ultima comparacion es exactamente el algoritmo de aproximacion de Sahni
(1975) para la mochila 0/1: el prefijo greedy no es optimo porque el elemento
critico "tapa" la capacidad sobrante, y quedarse con el critico solo garantiza
al menos la mitad del optimo. Por eso este archivo lo usan P1 (como algoritmo
de Sahni) y P3 (como linea base Greedy del TP1).

ADVERTENCIA sobre la version vista en clase: si la catedra presenta a Sahni con
el redondeo explicito de la cota de relajacion lineal, hay que confirmarlo
antes del informe; el codigo de aca es la version del TP1, que no calcula la
cota.

Diferencias deliberadas con el TP1 (dos, ambas corregidas aca):

1. Aquel ordenaba la lista de entrada en el lugar (`objetos.sort(...)`), con lo
   cual la segunda medicion del mismo algoritmo recibia la lista ya ordenada y
   el tiempo medido no era comparable. Aca se ordena una lista de indices.
2. Aquel devolvia el elemento critico aunque no entrara solo en la mochila: si
   `peso_critico > w`, la solucion resultante era infactible. No se disparaba
   con los sets del TP1 (w = n*50 contra pesos <= 200) pero si con cualquier
   instancia donde un elemento pese mas que la capacidad. Aca ese candidato
   solo se considera si entra.

Garantia: si `z*` es el optimo y `z_lp` la cota de relajacion lineal,
`valor >= z_lp - peso_critico` y `valor >= z*/2`.

Contrato de datos (el de `comun/parser_mochila.py`): `elems[i]` es el par
`(peso, beneficio)`, `n` la cantidad de elementos y `w` la capacidad.
"""

from __future__ import annotations


def greedy(elems, n: int, w: int, traza: list[str] | None = None) -> tuple[int, list[int]]:
    """Aproximacion por prefijo greedy + elemento critico.

    Devuelve `(valor, seleccion)`, con `seleccion` ordenada por indice.
    """
    orden = sorted(
        range(n),
        key=lambda i: elems[i][1] / elems[i][0],
        reverse=True,
    )

    peso_contador = 0
    beneficio_total = 0
    seleccion: list[int] = []
    critico: int | None = None

    for i in orden:
        peso, beneficio = elems[i]
        if peso_contador + peso <= w:
            peso_contador += peso
            beneficio_total += beneficio
            seleccion.append(i)
            if traza is not None:
                traza.append(
                    f"toma {i} (p={peso} b={beneficio}) "
                    f"-> peso {peso_contador}/{w} beneficio {beneficio_total}"
                )
        else:
            critico = i
            if traza is not None:
                traza.append(
                    f"critico {i} (p={peso} b={beneficio}) "
                    f"no entra: queda {w - peso_contador} de capacidad"
                )
            break

    if critico is not None:
        peso_critico, beneficio_critico = elems[critico]
        if peso_critico <= w and beneficio_critico > beneficio_total:
            seleccion = [critico]
            beneficio_total = beneficio_critico
            if traza is not None:
                traza.append(
                    f"el critico solo ({beneficio_total}) supera al prefijo "
                    f"-> se devuelve [elemento critico]"
                )
        elif traza is not None:
            traza.append(
                f"el prefijo ({beneficio_total}) supera al critico solo "
                f"-> se devuelve el prefijo de {len(seleccion)} elementos"
            )

    seleccion.sort()
    return beneficio_total, seleccion
