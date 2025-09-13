import pandas as pd
from collections import deque
import heapq

# ==========================
# 1. Cargar laberinto desde Excel
# ==========================
laberinto = pd.read_csv("laberinto.csv", header=None)
laberinto = laberinto.values  # convertir a matriz (numpy array)

# ==========================
# 2. Detectar inicio (S) y fin (E)
# ==========================
inicio, fin = None, None
for i in range(len(laberinto)):
    for j in range(len(laberinto[0])):
        if laberinto[i][j] == "S":
            inicio = (i, j)
        elif laberinto[i][j] == "E":
            fin = (i, j)

# ==========================
# 3. Movimientos posibles
# ==========================
movimientos = [(-1,0), (1,0), (0,-1), (0,1)]  # arriba, abajo, izq, der

# ==========================
# 4. DFS (Profundidad)
# ==========================
def dfs(laberinto, inicio, fin):
    stack = [inicio]
    visitados = set([inicio])
    padre = {inicio: None}

    while stack:
        nodo = stack.pop()
        if nodo == fin:
            break
        for mov in movimientos:
            vecino = (nodo[0]+mov[0], nodo[1]+mov[1])
            if (0 <= vecino[0] < len(laberinto) and
                0 <= vecino[1] < len(laberinto[0]) and
                laberinto[vecino[0]][vecino[1]] != 1 and
                vecino not in visitados):
                stack.append(vecino)
                visitados.add(vecino)
                padre[vecino] = nodo

    # reconstruir camino
    camino = []
    actual = fin
    while actual:
        camino.append(actual)
        actual = padre.get(actual)
    return camino[::-1]

# ==========================
# 5. BFS (Anchura)
# ==========================
def bfs(laberinto, inicio, fin):
    cola = deque([inicio])
    visitados = set([inicio])
    padre = {inicio: None}

    while cola:
        nodo = cola.popleft()
        if nodo == fin:
            break
        for mov in movimientos:
            vecino = (nodo[0]+mov[0], nodo[1]+mov[1])
            if (0 <= vecino[0] < len(laberinto) and
                0 <= vecino[1] < len(laberinto[0]) and
                laberinto[vecino[0]][vecino[1]] != 1 and
                vecino not in visitados):
                cola.append(vecino)
                visitados.add(vecino)
                padre[vecino] = nodo

    # reconstruir camino
    camino = []
    actual = fin
    while actual:
        camino.append(actual)
        actual = padre.get(actual)
    return camino[::-1]

# ==========================
# 6. A* (Heurística Manhattan)
# ==========================
def heuristica(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])  # distancia Manhattan

def a_star(laberinto, inicio, fin):
    open_set = []
    heapq.heappush(open_set, (0, inicio))
    g = {inicio: 0}
    padre = {inicio: None}

    while open_set:
        _, nodo = heapq.heappop(open_set)
        if nodo == fin:
            break
        for mov in movimientos:
            vecino = (nodo[0]+mov[0], nodo[1]+mov[1])
            if (0 <= vecino[0] < len(laberinto) and
                0 <= vecino[1] < len(laberinto[0]) and
                laberinto[vecino[0]][vecino[1]] != 1):
                costo = g[nodo] + 1
                if vecino not in g or costo < g[vecino]:
                    g[vecino] = costo
                    f = costo + heuristica(vecino, fin)
                    heapq.heappush(open_set, (f, vecino))
                    padre[vecino] = nodo

    # reconstruir camino
    camino = []
    actual = fin
    while actual:
        camino.append(actual)
        actual = padre.get(actual)
    return camino[::-1]

# ==========================
# 7. Probar algoritmos
# ==========================
camino_dfs = dfs(laberinto, inicio, fin)
camino_bfs = bfs(laberinto, inicio, fin)
camino_astar = a_star(laberinto, inicio, fin)

print("DFS encontró un camino de longitud:", len(camino_dfs))
print(camino_dfs)

print("\nBFS encontró un camino de longitud:", len(camino_bfs))
print(camino_bfs)

print("\nA* encontró un camino de longitud:", len(camino_astar))
print(camino_astar)
