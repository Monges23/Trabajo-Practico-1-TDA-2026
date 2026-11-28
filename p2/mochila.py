"""TP2 - Problema 2: esquema de aproximacion arbitrariamente bueno (FPTAS) para la mochila 0/1.

    b      = eps * vmax / (2n)
    k_i    = ceil(v_i / b)            (v_i redondeado hacia arriba a un multiplo de b, expresado en unidades de b)
    OPT[i][V] = peso minimo para lograr beneficio escalado V con los primeros i elementos

    Se devuelve el mayor V con OPT[n][V] <= W y la seleccion se reconstruye comparando
    filas: el elemento i se tomo si OPT[i][V] != OPT[i-1][V].
"""

from __future__ import annotations

from array import array

INF = 1 << 60

def _inversa_entera(eps: float) -> int:
    if eps <= 0:
        raise ValueError("epsilon debe ser positivo")
    m = round(1.0 / eps)
    if m < 1 or abs(1.0 / eps - m) > 1e-9:
        raise ValueError(
            "epsilon debe cumplir que 1/epsilon sea entero (ej: 1, 1/2, 1/5, 1/10)"
        )
    return m


def resolver(elems, n, w, eps):
    m = _inversa_entera(eps)

    idx = [i for i in range(n) if elems[i][0] <= w and elems[i][1] > 0]
    ne = len(idx)
    if ne == 0:
        return 0, []

    pesos = [elems[i][0] for i in idx]
    valores = [elems[i][1] for i in idx]

    vmax = max(valores)
    k = [-((-v * 2 * ne * m) // vmax) for v in valores]
    T = sum(k) 

    fila0 = array("q", [INF]) * (T + 1)
    fila0[0] = 0
    OPT = [fila0]
    alcance = 0
    for i in range(1, ne + 1):
        previa = OPT[i - 1]
        fila = array("q", previa)  
        ki, wi = k[i - 1], pesos[i - 1]
        hasta = alcance + ki
        for V in range(ki, hasta + 1): 
            candidato = previa[V - ki] + wi
            if candidato < fila[V]:
                fila[V] = candidato
        OPT.append(fila)
        alcance = hasta

    ultima = OPT[ne]
    V = alcance
    while ultima[V] > w:
        V -= 1

    seleccion = []
    for i in range(ne, 0, -1):
        if OPT[i][V] != OPT[i - 1][V]:
            seleccion.append(idx[i - 1])
            V -= k[i - 1]
    seleccion.sort()
    valor = sum(elems[i][1] for i in seleccion)

    return valor, seleccion



if __name__ == "__main__":
    import pathlib
    import sys
 
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from comun.exacto import dinamica
    from comun.parser_mochila import parsear_mochila

    if len(sys.argv) != 3:
        print("Uso: python3 p2/mochila.py <instancia.txt> <epsilon>   (ej: 0.1)")
        sys.exit(1)

    elems, n, w = parsear_mochila(sys.argv[1])
    eps = float(sys.argv[2])
    valor, seleccion = resolver(elems, n, w, eps)
    optimo = dinamica.valor_compacto(elems, n, w)
    print(f"epsilon = {eps}")
    print(f"Resultado FPTAS = {valor}   Optimo (PD del TP1) = {optimo}   Cociente = {valor / optimo:.5f}")
    print(f"Elementos elegidos: {len(seleccion)}   Peso usado: {sum(elems[i][0] for i in seleccion)} / {w}")
    