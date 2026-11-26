# Guía de estudio y defensa — TP2 Problema 1 (P1)

Documento de referencia para preparar la defensa oral y consolidar el diseño de `tp2/p1`. Resume el objetivo de la consigna en [TP02-2026-2c.pdf](file:///home/fballerio/uba/tda/tp2/TP02-2026-2c.pdf), el sentido teórico y práctico de las cotas superiores, el desarrollo matemático de cada método, un caso testigo completo, preguntas frecuentes de defensa y el estado actual del código en `tp2/`.

---

## 1. Resumen ejecutivo: qué pide el Problema 1

El Problema 1 pide **encerrar al óptimo exacto $z^*$** de la mochila 0/1 entre una solución factible aproximada (por abajo) y dos cotas superiores cada vez más ajustadas (por arriba), **calculando los cuatro valores sobre las mismas instancias** al variar el tamaño $n$:

$$z_{\text{Sahni}} \le z^* \le U_{\text{MT}} \le \lfloor U_{\text{LP}} \rfloor \le U_{\text{LP}}$$

| Magnitud | Rol en P1 | Relación con $z^*$ | Complejidad típica | Ubicación actual en `tp2/` |
| --- | --- | --- | --- | --- |
| $z_{\text{Sahni}}$ | Solución entera aproximada (factible) | $z_{\text{Sahni}} \le z^*$ | $O(n^{k+1})$ en el esquema $A_k$ ($k \ge 1$) / $O(n \log n)$ si $k=0$ o greedy $1/2$ | [greedy.py](file:///home/fballerio/uba/tda/tp2/comun/greedy.py) *(ver checklist §9)* |
| $z^*$ | Óptimo exacto (verdad de referencia del TP1) | $z^*$ | Exponencial o pseudopolinomial | [programacion_lineal.py](file:///home/fballerio/uba/tda/tp2/comun/exacto/programacion_lineal.py) / [experimento.py](file:///home/fballerio/uba/tda/tp2/p1/experimento.py) |
| $U_{\text{LP}}$ | Cota superior por relajación lineal (Dantzig) | $z^* \le \lfloor U_{\text{LP}} \rfloor \le U_{\text{LP}}$ | $O(n \log n)$ | [cotas.py](file:///home/fballerio/uba/tda/tp2/comun/cotas.py#L124-L152) |
| $U_{\text{MT}}$ | Cota superior entera de Martello y Toth ($U_2$) | $z^* \le U_{\text{MT}} \le \lfloor U_{\text{LP}} \rfloor$ | $O(n \log n)$ | [cotas.py](file:///home/fballerio/uba/tda/tp2/comun/cotas.py#L155-L214) |

La comparación de los cuatro valores responde dos preguntas concretas:

1. **Por abajo (calidad práctica del algoritmo aproximado):** cuánto más cerca de $z^*$ se ubica Sahni en instancias reales respecto de su garantía teórica de peor caso.
2. **Por arriba (ajuste de las cotas):** cuánto logra reducir $U_{\text{MT}}$ el exceso de $U_{\text{LP}}$ sin necesidad de resolver el problema entero.

Además, las **Condiciones Generales** (página 2 de [TP02-2026-2c.pdf](file:///home/fballerio/uba/tda/tp2/TP02-2026-2c.pdf)) exigen incluir para cada algoritmo: supuestos, pseudocódigo, detalle de estructuras de datos, seguimiento con un conjunto reducido, análisis de complejidad temporal a partir del pseudocódigo, archivos con los sets de datos y su criterio de selección, gráfico de tiempos medidos junto con la curva teórica de ajuste, e informe de resultados.

---

## 2. Notación base e ítem crítico ($s$)

Para formular ambas cotas y el completado voraz de Sahni, se ordenan los ítems por eficiencia (beneficio por unidad de peso) en orden no creciente:

$$\frac{p_1}{w_1} \ge \frac{p_2}{w_2} \ge \dots \ge \frac{p_n}{w_n}$$

A partir de ese orden, sobre una mochila de capacidad $W$, se definen:

- **Pesos y beneficios acumulados del prefijo:**
  $$W_k = \sum_{j=1}^{k} w_j, \qquad P_k = \sum_{j=1}^{k} p_j$$
- **Ítem crítico ($s$):** el primer índice del orden cuyo peso acumulado excede la capacidad $W$:
  $$W_{s-1} \le W < W_{s-1} + w_s$$
- **Capacidad residual ($r_c$):** el espacio libre que queda inmediatamente antes de intentar incorporar al ítem crítico $s$:
  $$r_c = W - W_{s-1} \qquad (0 \le r_c < w_s)$$

Esquema visual del prefijo hasta el ítem crítico:

```text
[ ítem 1 ] [ ítem 2 ] ... [ ítem s-1 ] |  hueco rc  |
|<-------------- W_{s-1} ------------->|<--- rc --->|
|<----------------------- W ----------------------->|
                                       ^
                                       aquí se intenta incluir a s (w_s > rc)
```

*(Caso borde: si $\sum_{j=1}^{n} w_j \le W$, todos los ítems caben enteros, no existe ítem crítico y tanto las cotas como el óptimo exacto coinciden con el beneficio total.)*

---

## 3. Sentido práctico y teórico de las cotas superiores

Calcular $U_{\text{LP}}$ y $U_{\text{MT}}$ junto con $z^*$ en P1 puede parecer redundante si ya se conoce el óptimo exacto. Sin embargo, las cotas superiores cumplen tres roles fundamentales:

### 3.1. Certificar calidad sin conocer el óptimo ($z^*$)
En instancias de gran escala (o con pesos y beneficios elevados), calcular $z^*$ puede resultar computacionalmente inviable. Si se ejecuta un algoritmo aproximado rápido y se obtiene una solución factible de valor $z_{\text{aprox}}$:

- La garantía teórica (por ejemplo $\frac{1}{2}$ o $\frac{k}{k+1}$) solo acota el peor caso posible, pero no informa qué tan buena fue la solución en esa instancia particular.
- Calculando una cota superior $U$ en $O(n \log n)$, se garantiza que $z_{\text{aprox}} \le z^* \le U$.
- Con ello se acota la distancia absoluta o relativa al óptimo ($z^* - z_{\text{aprox}} \le U - z_{\text{aprox}}$) sin haber calculado $z^*$. En el caso límite en que $z_{\text{aprox}} = U$, se obtiene un certificado de optimalidad exacta en tiempo $O(n \log n)$.

### 3.2. Podar árboles de búsqueda en algoritmos exactos
En métodos exactos como Backtracking, Branch & Bound o solvers de programación lineal entera, una cota superior permite descartar subárboles completos sin perder el óptimo:

$$\text{beneficio\_actual} + U(\text{subproblema restante}) \le \text{mejor\_solución\_conocida} \implies \text{podar rama}$$

Cuanto más baja (más ajustada) sea $U$, mayor cantidad de ramas se podan y menor es el tiempo de exploración.

### 3.3. Por qué se comparan Dantzig y Martello-Toth en el TP2
- **Relajación lineal ($U_{\text{LP}}$):** es la cota más natural, pero al fraccionar el ítem crítico $s$ puede quedar artificialmente alta respecto de las soluciones 0/1 reales.
- **Martello y Toth ($U_{\text{MT}}$):** corrige exactamente esa debilidad exigiendo $x_s \in \{0, 1\}$, mejorando o igualando a $\lfloor U_{\text{LP}} \rfloor$ con solo **$O(1)$ operaciones adicionales** tras localizar $s$.
- **Rol en el TP2:** en **P1** se usa $z^*$ para medir cuán cerca de la verdad quedan $U_{\text{MT}}$ y $U_{\text{LP}}$; en **P4**, cuando se comparen algoritmos en tamaños donde los métodos exactos no escalan, las cotas sirven como referencia superior para evaluar las aproximaciones.

---

## 4. Relajación lineal — Cota de Dantzig ($U_{\text{LP}}$)

### 4.1. Formulación y forma cerrada
La mochila 0/1 exige variables binarias $x_i \in \{0, 1\}$. La **relajación lineal** reemplaza esa restricción por $0 \le x_i \le 1$, transformando el problema en la mochila fraccionaria:

$$\max \sum_{i=1}^{n} p_i x_i \quad \text{s.a.} \quad \sum_{i=1}^{n} w_i x_i \le W, \quad 0 \le x_i \le 1$$

Como toda solución entera pertenece al dominio relajado, se cumple $z^* \le U_{\text{LP}}$. Por un argumento de intercambio voraz, el óptimo de este programa lineal no requiere un solver general (como Simplex en PuLP): se obtiene llenando en orden de eficiencia hasta el crítico $s$ y tomando la fracción $\frac{r_c}{w_s}$ de este:

$$U_{\text{LP}} = P_{s-1} + r_c \frac{p_s}{w_s}$$

### 4.2. Versión entera $\lfloor U_{\text{LP}} \rfloor$ y complejidad
- **Truncamiento a entero:** cuando todos los beneficios $p_i$ son enteros, el óptimo exacto $z^*$ también es entero. Cualquier parte fraccionaria de $U_{\text{LP}}$ es inalcanzable, por lo que $z^* \le \lfloor U_{\text{LP}} \rfloor$ sigue siendo una cota superior válida y estrictamente más informativa que el valor decimal.
- **Complejidad:** $O(n \log n)$ por el ordenamiento inicial por eficiencia (o $O(n)$ si los ítems ya vienen ordenados).
- **Debilidad principal:** si el ítem crítico $s$ tiene peso alto y eficiencia elevada, la relajación lineal aprovecha una porción grande de $s$ que en el problema 0/1 no puede dividirse.

### 4.3. Cuidados numéricos y de borde (observados en `comun/cotas.py`)
En [cotas.py](file:///home/fballerio/uba/tda/tp2/comun/cotas.py#L71-L152) se contemplan dos detalles críticos para preservar la validez matemática de la cota:

1. **Sin punto flotante al ordenar ni truncar:** las eficiencias se comparan mediante producto cruzado entero (`p_i * w_j` contra `p_j * w_i`) con desempate determinístico por índice, y la parte entera se calcula con división entera `(r_c * p_s) // w_s`. Usar `math.floor` sobre flotantes puede convertir un cociente entero exacto $k$ en `k - 1e-16` y reducir la cota a $k - 1$, invalidándola.
2. **Ítems con $w_i > W$:** en el LP continuo puro (como en PuLP con $0 \le x_i \le 1$), un ítem con peso mayor a la capacidad $W$ puede ingresar de forma fraccionaria ($x_i = W / w_i < 1$). Por eso la cota de Dantzig no los filtra si se desea equivalencia exacta con el LP continuo, mientras que una solución 0/1 nunca puede incluirlos.

---

## 5. Cota de Martello y Toth ($U_{\text{MT}}$ / $U_2$)

### 5.1. Qué tipo de algoritmo utiliza
En el Problema 1 del TP2, Martello y Toth **no es un algoritmo de búsqueda ni un método exacto** (no ejecuta Backtracking, Branch & Bound, Programación Dinámica ni un solver de PL). Se trata de una **fórmula cerrada de cota superior** ($U_2$ en Martello y Toth, 1990) calculada mediante un procedimiento determinístico directo:

1. **Filtrado de ítems inviables ($w_i > W$):** $O(n)$.
2. **Ordenamiento por eficiencia no creciente:** $O(n \log n)$.
3. **Barrido lineal para hallar $s$, $W_{s-1}$, $P_{s-1}$ y $r_c$:** $O(n)$.
4. **Evaluación de dos fórmulas aritméticas ($U^0$ y $U^1$) y retorno del máximo:** $O(1)$.

**Complejidad total:** $O(n \log n)$ (y $O(n)$ sobre una entrada ya ordenada).

*(Nota histórica para evitar confusiones en la defensa: Martello y Toth sí diseñaron los algoritmos exactos de **Branch & Bound** denominados MT1 y MT2, pero en P1 se implementa únicamente la cota superior $U_2$ que ellos desarrollaron para acotar ramas dentro de esos árboles.)*

### 5.2. Idea central y descomposición en dos universos
La cota $U_{\text{MT}}$ ataca el punto débil de $U_{\text{LP}}$: en la solución óptima entera $x^*$, el ítem crítico $s$ no puede tomar un valor fraccionario; necesariamente cumple $x^*_s = 0$ o $x^*_s = 1$:

$$z^* = \max\!\left(z^*_{x_s = 0},\; z^*_{x_s = 1}\right)$$

Acotando cada universo por separado con una relajación continua y tomando el máximo de ambos techos, se obtiene una cota superior válida para $z^*$.

#### Universo A: el crítico queda excluido ($x_s = 0$)
Se conserva la relajación fraccionaria sobre $\{1, \dots, n\} \setminus \{s\}$. El prefijo $1 \dots s-1$ entra entero (beneficio $P_{s-1}$) y la capacidad residual $r_c$ debe cubrirse usando ítems posteriores a $s$. Como el orden es no creciente en eficiencia, ningún ítem disponible supera la tasa $\frac{p_{s+1}}{w_{s+1}}$:

$$U^0 = P_{s-1} + \left\lfloor r_c \frac{p_{s+1}}{w_{s+1}} \right\rfloor$$

*(Si $s = n$, no existe ítem $s+1$ y se toma $U^0 = P_{s-1}$.)*

#### Universo B: el crítico entra completo ($x_s = 1$)
Es frecuente dudar de cómo puede incluirse el ítem crítico $s$ si justamente fue definido como el primero que no cabía tras $1 \dots s-1$. La respuesta es que **$U_{\text{MT}}$ acota al óptimo global $z^*$, no al recorrido greedy**: el óptimo real no está obligado a conservar todo el prefijo $1 \dots s-1$, y puede incluir al ítem $s$ retirando uno o más ítems anteriores.

Al fijar $x_s = 1$, la capacidad disponible para los demás ítems pasa a ser $W - w_s$. Comparada contra el peso del prefijo completo $W_{s-1} = W - r_c$, la cantidad mínima de peso que debe retirarse de $\{1, \dots, s-1\}$ es:

$$W_{s-1} - (W - w_s) = w_s - r_c > 0$$

Para obtener un techo optimista en tiempo $O(1)$ sin reexplorar el prefijo, se asume que todo ese excedente de peso $w_s - r_c$ se libera al **menor costo por unidad de peso posible** dentro de $\{1, \dots, s-1\}$, que corresponde al último ítem del prefijo ($s-1$, con tasa $\frac{p_{s-1}}{w_{s-1}}$):

$$U^1 = P_{s-1} + \left\lfloor p_s - (w_s - r_c)\frac{p_{s-1}}{w_{s-1}} \right\rfloor$$

**¿Por qué $U^1$ sigue siendo válida si $w_{s-1} < w_s - r_c$ (es decir, si retirar al ítem $s-1$ entero no alcanza)?**
Porque en ese caso la solución óptima tendría que quitar peso de ítems anteriores ($s-2, s-3, \dots$), cuya eficiencia es **mayor o igual** a $\frac{p_{s-1}}{w_{s-1}}$, perdiendo todavía más beneficio por unidad de peso. Descontar todo el faltante a la tarifa más barata $\frac{p_{s-1}}{w_{s-1}}$ resta menos beneficio que el sacrificio real, por lo que $U^1$ permanece por encima o igual de $z^*_{x_s=1}$.

#### Cota final
Como no se conoce de antemano en cuál de los dos universos reside el óptimo exacto, se toma el mayor de ambos techos:

$$U_{\text{MT}} = \max(U^0, U^1)$$

### 5.3. Por qué siempre cumple $z^* \le U_{\text{MT}} \le \lfloor U_{\text{LP}} \rfloor$
1. **Validez respecto de $z^*$ ($z^* \le U_{\text{MT}}$):**
   - Si $x^*_s = 0$, la solución óptima es factible para el problema lineal sin $s$, cuyo valor máximo no excede $P_{s-1} + r_c \frac{p_{s+1}}{w_{s+1}}$. Con beneficios enteros, $z^* = z^*_{x_s=0} \le U^0$.
   - Si $x^*_s = 1$, la solución óptima sin $s$ cabe en capacidad $W - w_s < W_{s-1}$; su relajación fraccionaria sobre $\{1, \dots, n\} \setminus \{s\}$ debe liberar al menos $w_s - r_c$ de peso del prefijo $\{1, \dots, s-1\}$ pagando como mínimo $\frac{p_{s-1}}{w_{s-1}}$ por unidad, de modo que $z^* = z^*_{x_s=1} \le U^1$.
   - Por lo tanto, $z^* = \max(z^*_{x_s=0}, z^*_{x_s=1}) \le \max(U^0, U^1) = U_{\text{MT}}$.

2. **Dominancia sobre la relajación lineal ($U_{\text{MT}} \le \lfloor U_{\text{LP}} \rfloor$):**
   - Para $U^0$: como $\frac{p_{s+1}}{w_{s+1}} \le \frac{p_s}{w_s}$ y $r_c \ge 0$, se tiene $P_{s-1} + r_c \frac{p_{s+1}}{w_{s+1}} \le U_{\text{LP}}$, y al truncar resulta $U^0 \le \lfloor U_{\text{LP}} \rfloor$.
   - Para $U^1$: como $\frac{p_{s-1}}{w_{s-1}} \ge \frac{p_s}{w_s}$ y $w_s - r_c > 0$:
     $$p_s - (w_s - r_c)\frac{p_{s-1}}{w_{s-1}} \le p_s - (w_s - r_c)\frac{p_s}{w_s} = r_c \frac{p_s}{w_s}$$
     Sumando $P_{s-1}$ y aplicando piso entero, resulta $U^1 \le \lfloor U_{\text{LP}} \rfloor$.

### 5.4. Precondición y comportamiento según las instancias
- **Precondición $w_j \le W$:** requiere filtrar previamente los ítems con peso mayor que $W$. Sin ese filtro, el primer ítem por eficiencia podría superar la capacidad ($s = 1$), en cuyo caso no existiría el ítem $s - 1$ necesario para $U^1$.
- **Cuándo mejora mucho a $U_{\text{LP}}$ y cuándo no:** cuando hay saltos marcados de eficiencia alrededor del crítico ($\frac{p_{s-1}}{w_{s-1}} \gg \frac{p_s}{w_s} \gg \frac{p_{s+1}}{w_{s+1}}$), ambas penalizaciones recortan significativamente la cota. En cambio, en instancias uniformes grandes (donde los ítems cercanos a $s$ tienen eficiencias casi idénticas) o en instancias de *subset-sum* (donde $p_i/w_i = 1$ para todo $i$), tanto $U^0$ como $U^1$ tienden a coincidir con $\lfloor U_{\text{LP}} \rfloor$.

---

## 6. Algoritmo de Sahni (1975) — Esquema $A_k$

### 6.1. Problema que resuelve respecto del greedy puro
El algoritmo greedy clásico (incorporar en orden de $p_i/w_i$ mientras quepa) puede obtener resultados arbitrariamente malos frente al óptimo. Con $W = 100$ e ítems $(w_1=1, p_1=2)$ y $(w_2=100, p_2=100)$, el greedy elige el primer ítem (beneficio $2$), bloqueando al segundo (beneficio $100$). El greedy modificado con garantía $\frac{1}{2}$ del TP1 corrige el caso de un único ítem grande comparando el prefijo contra un ítem individual, pero no resuelve combinaciones de varios ítems medianos o grandes.

### 6.2. Funcionamiento del esquema $A_k$
En *Approximate Algorithms for the 0/1 Knapsack Problem* (1975), Sahni parametriza la aproximación mediante un entero fijo $k \ge 0$ que combina fuerza bruta acotada sobre hasta $k$ ítems con completado voraz:

1. Ordenar los $n$ ítems por eficiencia $p_i / w_i$ en orden no creciente.
2. Iterar sobre todo subconjunto $M \subseteq \{1, \dots, n\}$ tal que $|M| \le k$ y $w(M) = \sum_{i \in M} w_i \le W$.
3. Para cada $M$ factible:
   - Inicializar la mochila con $M$ y capacidad restante $R = W - w(M)$.
   - Recorrer los ítems restantes $\{1, \dots, n\} \setminus M$ en orden de eficiencia decreciente, agregando cada ítem $i$ que cumpla $w_i \le R$ y actualizando $R \leftarrow R - w_i$ (sin detenerse en el primero que no entra: se evalúan todos hasta el final).
4. Devolver la mejor solución hallada entre todos los subconjuntos $M$.

### 6.3. Demostración de la garantía $z_{A_k} > \frac{k}{k+1} z^*$ (para $k \ge 1$)
Sea $O$ una solución óptima de valor $z^*$.

1. **Caso $|O| \le k$:** el algoritmo evalúa explícitamente $M = O$ y devuelve el óptimo exacto ($z_{A_k} = z^*$).
2. **Caso $|O| > k$:** sea $M^* \subset O$ el subconjunto formado por los **$k$ ítems de mayor beneficio** de $O$. Como $|M^*| = k$ y $w(M^*) \le W$, el algoritmo evalúa $M^*$ y ejecuta el completado voraz $G$ sobre $\{1, \dots, n\} \setminus M^*$ con capacidad restante $R = W - w(M^*)$.
3. Si el completado voraz acepta todos los ítems de $O \setminus M^*$, entonces $p(G) \ge p(O \setminus M^*)$ y $z_{A_k} = z^*$. En caso contrario, sea $j^*$ el **primer** ítem de $O \setminus M^*$ (en orden de eficiencia) que es rechazado por no caber en la capacidad disponible, y sea $G_1 \subseteq G$ el conjunto de ítems aceptados por el voraz antes de evaluar $j^*$.
   - Como el recorrido sigue el orden de eficiencia y $w(G_1) + w_{j^*} > R$, el conjunto $G_1$ junto con una fracción $\theta = \frac{R - w(G_1)}{w_{j^*}} \in [0, 1)$ del ítem $j^*$ constituye el óptimo de la relajación lineal sobre los ítems disponibles $\{1, \dots, n\} \setminus M^*$ para capacidad $R$.
   - Dado que $O \setminus M^*$ es una solución entera factible para ese mismo subproblema de capacidad $R$, su beneficio está acotado por dicho óptimo fraccionario:
     $$p(O \setminus M^*) \le p(G_1) + \theta p_{j^*} < p(G_1) + p_{j^*} \le p(G) + p_{j^*}$$
   - Sumando $p(M^*)$ a ambos miembros:
     $$z^* = p(M^*) + p(O \setminus M^*) < p(M^*) + p(G) + p_{j^*} \le z_{A_k} + p_{j^*} \implies z^* - z_{A_k} < p_{j^*}$$
4. Por construcción, los $k$ ítems de $M^*$ tienen cada uno beneficio mayor o igual que $p_{j^*}$ (ya que $j^* \in O \setminus M^*$). Al ser $k+1$ ítems distintos dentro de $O$:
   $$(k + 1)\,p_{j^*} \le p(M^*) + p_{j^*} \le p(O) = z^* \implies p_{j^*} \le \frac{z^*}{k+1}$$

Combinando ambos resultados:

$$z_{A_k} > z^* - \frac{z^*}{k+1} = \frac{k}{k+1}\,z^*$$

### 6.4. Complejidad temporal, espacial y puente con el Problema 2
- **Complejidad temporal:** ordenar los ítems cuesta $O(n \log n)$. La cantidad de subconjuntos de tamaño a lo sumo $k$ es $\sum_{j=0}^{k} \binom{n}{j} = O(n^k)$, y cada completado voraz recorre a lo sumo $n$ elementos en $O(n)$. Para todo $k \ge 1$ fijo, el costo total es $O(n^{k+1})$.
- **Complejidad espacial:** $O(n)$ (solo se mantienen los vectores ordenados, la solución en curso y la mejor solución encontrada).
- **Relación con $k$ y diferencia con el P2 (FPTAS):**
  - $k = 1$: garantía $> \frac{1}{2} z^*$ en $O(n^2)$.
  - $k = 2$: garantía $> \frac{2}{3} z^*$ en $O(n^3)$.
  - Para garantizar un error relativo a lo sumo $\varepsilon$ (es decir, $z \ge (1 - \varepsilon) z^*$), se requiere $\frac{k}{k+1} \ge 1 - \varepsilon$, es decir $k = \lceil 1/\varepsilon \rceil - 1$. Esto da tiempo $O(n^{\lceil 1/\varepsilon \rceil})$: es un **PTAS** (*Polynomial-Time Approximation Scheme*), polinomial en $n$ para $\varepsilon$ fijo, pero **exponencial en $1/\varepsilon$**.
  - Justamente esa limitación motiva el **Problema 2** del TP2 ("algoritmo arbitrariamente bueno", esquema de Ibarra y Kim, 1975): mediante escalado de beneficios y la programación dinámica alternativa del TP1, se logra un **FPTAS** (*Fully Polynomial-Time Approximation Scheme*), que es polinomial tanto en $n$ como en $1/\varepsilon$.

---

## 7. Ejemplo numérico completo ($n = 4,\; W = 10$)

Instancia con 4 ítems ya ordenados por eficiencia $p_i / w_i$:

| Ítem | Peso $w_i$ | Beneficio $p_i$ | Eficiencia $p_i / w_i$ |
| :---: | :---: | :---: | :---: |
| 1 | 2 | 19 | 9.5 |
| 2 | 5 | 30 | 6.0 |
| 3 | 5 | 21 | 4.2 |
| 4 | 4 | 4 | 1.0 |

### 7.1. Prefijo e ítem crítico
- Ítem 1: $W_1 = 2 \le 10$, $P_1 = 19$.
- Ítem 2: $W_2 = 2 + 5 = 7 \le 10$, $P_2 = 19 + 30 = 49$.
- Ítem 3: $W_2 + w_3 = 7 + 5 = 12 > 10 \implies$ **ítem crítico $s = 3$**, capacidad residual $r_c = 10 - 7 = 3$.

### 7.2. Cálculo de cotas, óptimo exacto y aproximaciones
1. **Relajación lineal ($U_{\text{LP}}$):** incorpora $\{1, 2\}$ y la fracción $\frac{3}{5}$ del ítem 3:
   $$U_{\text{LP}} = 49 + 3 \cdot \frac{21}{5} = 49 + 12.6 = 61.6 \implies \lfloor U_{\text{LP}} \rfloor = 61$$
2. **Martello y Toth ($U_{\text{MT}}$):**
   - **Rama $x_3 = 0$:** cubre $r_c = 3$ a la eficiencia del ítem 4 ($\frac{4}{4} = 1$):
     $$U^0 = 49 + \left\lfloor 3 \cdot \frac{4}{4} \right\rfloor = 52$$
   - **Rama $x_3 = 1$:** al incluir el ítem 3 ($w_3 = 5, p_3 = 21$), sobra $w_3 - r_c = 5 - 3 = 2$ de peso que se descuenta a la eficiencia del ítem 2 ($\frac{30}{5} = 6$):
     $$U^1 = 49 + \left\lfloor 21 - 2 \cdot \frac{30}{5} \right\rfloor = 49 + \lfloor 21 - 12 \rfloor = 58$$
   - **Resultado:** $U_{\text{MT}} = \max(52, 58) = 58$ (recorta 3 unidades enteras respecto de $\lfloor U_{\text{LP}} \rfloor$).
3. **Óptimo exacto ($z^*$):** la combinación $\{2, 3\}$ pesa $5 + 5 = 10 \le 10$ y alcanza $30 + 21 = 51$ (ningún otro subconjunto factible supera 49). Nótese que el óptimo **sí incluye al crítico $s = 3$** a costa de excluir al ítem 1 del prefijo.
4. **Aproximaciones (Greedy / Sahni $A_k$):**
   - **Greedy estándar y Greedy $1/2$ del TP1:** seleccionan $\{1, 2\}$ con valor $49$.
   - **Sahni $A_1$ ($k = 1$):** al fijar cada singleton ($M \in \{\emptyset, \{1\}, \{2\}, \{3\}, \{4\}\}$) y completar vorazmente, obtiene como máximo $49$ (por ejemplo, para $M = \{3\}$ con $R = 5$, el voraz prefiere al ítem 1 antes que al 2 y queda en $\{1, 3\} = 40$).
   - **Sahni $A_2$ ($k = 2$):** evalúa $M = \{2, 3\}$ ($w = 10, R = 0$) y encuentra el óptimo exacto $51$.

### 7.3. Comparación final sobre la instancia
$$49\;(\text{Greedy } / \; A_1) < 51\;(A_2 = z^*) < 58\;(U_{\text{MT}}) < 61\;(\lfloor U_{\text{LP}} \rfloor) < 61.6\;(U_{\text{LP}})$$

---

## 8. Preguntas frecuentes de defensa oral (Q&A)

**1. ¿Qué sentido tiene calcular las cotas de Dantzig y Martello-Toth si en P1 ya calculamos el óptimo exacto?**
En P1 el óptimo exacto $z^*$ funciona como referencia para medir experimentalmente cuánto se acercan las aproximaciones por debajo y cuán ajustadas resultan las cotas por arriba al crecer $n$. En escenarios donde el exacto es demasiado costoso (como en P4 o en instancias de gran escala), una cota superior calculada en $O(n \log n)$ permite acotar el error máximo de una solución aproximada sin conocer $z^*$, además de servir como función de poda en algoritmos exactos de Branch & Bound.

**2. En $U^1$, ¿cómo puede incluirse el ítem crítico $s$ si justamente fue el primero que no entró tras el prefijo $1 \dots s-1$?**
Porque la cota no restringe las soluciones al prefijo greedy. El óptimo entero global $x^*$ puede incluir a $s$ siempre que retire uno o más ítems de $\{1, \dots, s-1\}$ para liberar al menos $w_s - r_c$ de peso. Como todo ítem del prefijo tiene eficiencia $\ge \frac{p_{s-1}}{w_{s-1}}$, descontar ese peso a la tarifa del ítem $s-1$ subestima el beneficio sacrificado (incluso si $w_{s-1} < w_s - r_c$) y produce un techo válido en $O(1)$.

**3. ¿Qué tipo de algoritmo implementa Martello y Toth en P1? ¿Es Branch & Bound?**
No. En P1 no se implementa ninguno de los algoritmos exactos Branch & Bound de Martello y Toth (MT1 / MT2), sino únicamente su cota superior $U_2$. Es un cálculo directo y determinístico en $O(n \log n)$: filtrar $w_i \le W$, ordenar por eficiencia, hallar $s$ en un barrido lineal y tomar $\max(U^0, U^1)$ en tiempo constante.

**4. ¿Por qué en los resultados preliminares de P1 las cotas $U_{\text{MT}}$ y $U_{\text{LP}}$ dan valores tan cercanos al crecer $n$?**
En instancias no correlacionadas generadas uniformemente, al crecer $n$ la distribución de eficiencias alrededor del ítem crítico $s$ se vuelve muy densa ($\frac{p_{s-1}}{w_{s-1}} \approx \frac{p_s}{w_s} \approx \frac{p_{s+1}}{w_{s+1}}$). Como las penalizaciones de $U^0$ y $U^1$ dependen de las diferencias entre esas pendientes consecutivas, ambas cotas convergen hacia $\lfloor U_{\text{LP}} \rfloor$ (en las corridas actuales a $n = 200$, $U_{\text{MT}} \approx 1.000237\,z^*$ y $U_{\text{LP}} \approx 1.000244\,z^*$). Por el contrario, en instancias correlacionadas o con saltos de eficiencia alrededor de $s$, la diferencia entre ambas se vuelve visible.

**5. ¿En qué se diferencia el algoritmo de Sahni (1975) del algoritmo del Problema 2?**
El esquema $A_k$ de Sahni (1975) es un **PTAS** con complejidad $O(n^{k+1}) = O(n^{\lceil 1/\varepsilon \rceil})$: es polinomial en $n$ cuando $\varepsilon$ está fijo, pero exponencial en $1/\varepsilon$. En cambio, el algoritmo del Problema 2 (Ibarra y Kim, 1975) es un **FPTAS** que escala beneficios y aplica programación dinámica para ser polinomial tanto en $n$ como en $1/\varepsilon$.

---

## 9. Checklist de auditoría sobre el estado actual en `tp2/`

Al revisar la implementación existente en el repositorio frente a [TP02-2026-2c.pdf](file:///home/fballerio/uba/tda/tp2/TP02-2026-2c.pdf) y [TP01-2026-2.pdf](file:///home/fballerio/uba/tda/tp1/TP01-2026-2.pdf), quedan los siguientes puntos abiertos para verificar o corregir antes de la entrega:

- [ ] **Confirmar la definición de Sahni (1975) dada en clase:** hoy [greedy.py](file:///home/fballerio/uba/tda/tp2/comun/greedy.py#L93-L94) define `sahni = greedy` (el mismo Greedy con garantía $1/2$ del TP1 Ej 2). Sin embargo, el TP2 P4 lista por separado `"Greedy (aproximado)"` (TP1 Ej 2) y `"Algoritmo aproximado 1"` (TP2 P1), por lo que corresponde verificar con los apuntes del curso si P1 requiere el esquema $A_k$ de Sahni (1975) con parámetro $k$.
- [ ] **Corregir caso borde en [greedy.py](file:///home/fballerio/uba/tda/tp2/comun/greedy.py#L52-L75):** si el ítem de mayor eficiencia tiene $w_i > W$, el bucle corta en la primera iteración con prefijo vacío (`beneficio_total = 0`) y la validación posterior descarta al ítem crítico por inviable, devolviendo `0` aunque otros ítems sí quepan. Además, la prueba en [humo.py](file:///home/fballerio/uba/tda/tp2/comun/pruebas/humo.py#L103) usa `pesos=[10, 1], capacidad=10`, por lo que no ejercita un ítem con $w_i > W$.
- [ ] **Evaluar familias de instancias adicionales y persistir datasets en `tp2/datos/`:** las corridas actuales usan solo instancias uniformes no correlacionadas generadas en memoria; con $n \ge 50$, $U_{\text{MT}}$ y $U_{\text{LP}}$ casi empatan en [p1_resumen_por_tamano.csv](file:///home/fballerio/uba/tda/tp2/p1/resultados/tablas/p1_resumen_por_tamano.csv). Además, la entrega exige adjuntar los archivos de sets de datos utilizados.
- [ ] **Agregar curva teórica de ajuste en los gráficos de tiempos:** [informe.py](file:///home/fballerio/uba/tda/tp2/p1/informe.py#L224-L257) grafica solo los tiempos medidos, sin la curva teórica requerida por las Condiciones Generales (punto 6), y en $n \le 200$ los tiempos de microsegundos están dominados por ruido de medición (además de fijar la columna `tiempo_optimo_pl`, lo que omite el tiempo exacto cuando se corre con `--exacto pd`).
- [ ] **Incluir seguimiento paso a paso para el informe:** `greedy(inst, traza=[])` ya contempla el registro de pasos, pero falta generar el seguimiento completo (incluido el cálculo de $s$, $U_{\text{LP}}$ y $U_{\text{MT}}$) sobre un caso reducido.
