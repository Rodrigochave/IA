import pandas as pd
from collections import deque
import heapq
from copy import deepcopy
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# ==========================
# 1. Cargar laberinto desde CSV
# ==========================
df = pd.read_csv("C:/Users/Rorro/Documents/GitHub/IA/1er Parcial/laberinto.csv", header=None)
laberinto = df.values.tolist()

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
                str(laberinto[vecino[0]][vecino[1]]) != "1" and
                vecino not in visitados):
                stack.append(vecino)
                visitados.add(vecino)
                padre[vecino] = nodo

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
                str(laberinto[vecino[0]][vecino[1]]) != "1" and
                vecino not in visitados):
                cola.append(vecino)
                visitados.add(vecino)
                padre[vecino] = nodo

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
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

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
                str(laberinto[vecino[0]][vecino[1]]) != "1"):
                costo = g[nodo] + 1
                if vecino not in g or costo < g[vecino]:
                    g[vecino] = costo
                    f = costo + heuristica(vecino, fin)
                    heapq.heappush(open_set, (f, vecino))
                    padre[vecino] = nodo

    camino = []
    actual = fin
    while actual:
        camino.append(actual)
        actual = padre.get(actual)
    return camino[::-1]

# ==========================
# 7. Guardar recorridos en Excel con colores
# ==========================
def marcar_camino(laberinto, camino, nombre_algoritmo, archivo="recorridos.xlsx"):
    lab_copia = deepcopy(laberinto)
    for (i, j) in camino:
        if lab_copia[i][j] not in ["S", "E"]:  # no sobreescribir inicio y fin
            lab_copia[i][j] = "*"
    df = pd.DataFrame(lab_copia)

    # Guardar hoja en Excel
    try:
        with pd.ExcelWriter(archivo, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=nombre_algoritmo, header=False, index=False)
    except FileNotFoundError:
        with pd.ExcelWriter(archivo, mode="w", engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=nombre_algoritmo, header=False, index=False)

    # Abrir archivo para colorear celdas
    wb = load_workbook(archivo)
    ws = wb[nombre_algoritmo]
    verde = PatternFill(start_color="90EE90", end_color="90EE90", fill_type="solid")

    for (i, j) in camino:
        celda = ws.cell(row=i+1, column=j+1)  # +1 por índice Excel
        celda.fill = verde

    wb.save(archivo)

# ==========================
# 8. Ejecutar algoritmos y guardar
# ==========================
camino_dfs = dfs(laberinto, inicio, fin)
camino_bfs = bfs(laberinto, inicio, fin)
camino_astar = a_star(laberinto, inicio, fin)

print("DFS encontró un camino de longitud:", len(camino_dfs))
print("BFS encontró un camino de longitud:", len(camino_bfs))
print("A* encontró un camino de longitud:", len(camino_astar))

# Guardar en Excel con colores
archivo_salida = "recorridos.xlsx"
marcar_camino(laberinto, camino_dfs, "DFS", archivo_salida)
marcar_camino(laberinto, camino_bfs, "BFS", archivo_salida)
marcar_camino(laberinto, camino_astar, "A", archivo_salida)

print(f"\nSe guardaron los recorridos en {archivo_salida}")
