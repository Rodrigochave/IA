import csv
import heapq

def load_maze(filename):
    with open(filename, 'r', newline='', encoding='utf-8-sig') as file:  # Usar utf-8-sig para eliminar BOM
        reader = csv.reader(file)
        maze = []
        for row in reader:
            # Limpiar cada celda eliminando espacios y caracteres especiales
            cleaned_row = [cell.strip().replace('"', '').replace("'", "") for cell in row]
            maze.append(cleaned_row)
    return maze

def find_start_end(maze):
    start = None
    end = None
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i, j)
            elif cell == 'E':
                end = (i, j)
    
    if start is None:
        raise ValueError("No se encontró el punto de inicio 'S'")
    if end is None:
        raise ValueError("No se encontró el punto final 'E'")
    
    return start, end

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(maze, start, end):
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    open_list = []
    heapq.heappush(open_list, (0, start))
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    came_from = {}
    closed_set = set()

    while open_list:
        _, current = heapq.heappop(open_list)
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        closed_set.add(current)
        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Verificar límites del laberinto
            if not (0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0])):
                continue
            
            # Verificar si es obstáculo
            if maze[neighbor[0]][neighbor[1]] == '1':
                continue
                
            tentative_g = g_score[current] + 1
            
            if neighbor in closed_set and tentative_g >= g_score.get(neighbor, float('inf')):
                continue
                
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))
    
    return None

def main():
    try:
        maze = load_maze('C:/Users/Rodri/OneDrive/Documentos/GitHub/IA/1er Parcial/laberinto.csv')
        print(f"Laberinto cargado. Dimensiones: {len(maze)}x{len(maze[0])}")
        
        start, end = find_start_end(maze)
        print(f"Inicio encontrado en: {start}")
        print(f"Fin encontrado en: {end}")
        
        path = a_star(maze, start, end)
        
        if path:
            print("Camino encontrado:")
            for step in path:
                print(step)
            
            # Marcar el camino en el laberinto
            for i, j in path:
                if maze[i][j] not in ['S', 'E']:
                    maze[i][j] = '*'
            
            # Imprimir laberinto con el camino
            print("\nLaberinto con solución:")
            for row in maze:
                print(' '.join(row))
        else:
            print("No se encontró un camino válido.")
            
    except FileNotFoundError:
        print("Error: No se pudo encontrar el archivo 'laberinto.csv'")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()