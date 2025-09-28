import tkinter as tk
N = 3          # Tamaño del tablero (4x4)
MAX_DEPTH = 5   # Profundidad máxima de búsqueda del algoritmo Minimax

# =============================================================================
# BLOQUE 1: DETECCIÓN DE GANADOR
# =============================================================================
def check_winner(board):
    """
    Verifica si hay un ganador en el tablero.
    Retorna: +1 (gana X), -1 (gana O), 0 (empate), None (juego continúa)
    """
    # Verificar FILAS - Comprueba cada fila horizontalmente
    for i in range(N):
        if all(board[i][j] == "X" for j in range(N)): 
            return +1  # Fila completa con X
        if all(board[i][j] == "O" for j in range(N)): 
            return -1  # Fila completa con O
    
    # Verificar COLUMNAS - Comprueba cada columna verticalmente  
    for j in range(N):
        if all(board[i][j] == "X" for i in range(N)): 
            return +1  # Columna completa con X
        if all(board[i][j] == "O" for i in range(N)): 
            return -1  # Columna completa con O
    
    # Verificar DIAGONAL PRINCIPAL (de arriba-izquierda a abajo-derecha)
    if all(board[i][i] == "X" for i in range(N)): 
        return +1
    if all(board[i][i] == "O" for i in range(N)): 
        return -1
    
    # Verificar DIAGONAL SECUNDARIA (de arriba-derecha a abajo-izquierda)
    if all(board[i][N-1-i] == "X" for i in range(N)): 
        return +1
    if all(board[i][N-1-i] == "O" for i in range(N)): 
        return -1
    
    # Verificar EMPATE - si no hay espacios vacíos
    if all(board[i][j] != " " for i in range(N) for j in range(N)):
        return 0
    
    # Si no hay ganador y aún hay espacios vacíos
    return None

# =============================================================================
# BLOQUE 2: EVALUACIÓN HEURÍSTICA
# =============================================================================
def evaluate_line(line, board):
    """
    Evalúa una línea (fila, columna o diagonal) y le asigna un puntaje.
    Una línea con solo X tiene valor positivo, con solo O tiene valor negativo.
    """
    x_count = sum(1 for i, j in line if board[i][j] == "X")
    o_count = sum(1 for i, j in line if board[i][j] == "O")
    
    # Si la línea solo tiene X (sin O)
    if o_count == 0:
        return 10 ** x_count if x_count > 0 else 0  # 10^1=10, 10^2=100, 10^3=1000
    
    # Si la línea solo tiene O (sin X)  
    elif x_count == 0:
        return -10 ** o_count if o_count > 0 else 0  # -10^1=-10, -10^2=-100, etc.
    
    # Si la línea tiene mezcla de X y O (no es prometedora para nadie)
    return 0

def evaluate_board(board):
    """
    Evalúa el estado completo del tablero usando una función heurística.
    Suma los valores de todas las líneas posibles.
    """
    score = 0
    
    # Evaluar todas las FILAS y COLUMNAS
    for i in range(N):
        # Evaluar fila i
        score += evaluate_line([(i, j) for j in range(N)], board)
        # Evaluar columna i  
        score += evaluate_line([(j, i) for j in range(N)], board)
    
    # Evaluar DIAGONALES
    score += evaluate_line([(i, i) for i in range(N)], board)           # Diagonal principal
    score += evaluate_line([(i, N-1-i) for i in range(N)], board)      # Diagonal secundaria
    
    return score

# =============================================================================
# BLOQUE 3: ORDENAMIENTO PARA OPTIMIZAR PODA ALFA-BETA
# =============================================================================
def get_move_priority(i, j, board):
    """
    Asigna una prioridad a cada movimiento posible para ORDENARLOS.
    Esto optimiza la poda alfa-beta evaluando los mejores movimientos primero.
    """
    priority = 0
    
    # PRIORIDAD MÁXIMA: Movimiento que GANA el juego inmediatamente
    test_board = [row[:] for row in board]  # Copia del tablero
    test_board[i][j] = "X"  # Probar movimiento de X
    if check_winner(test_board) == 1:  # Si X gana con este movimiento
        return 10000  # Prioridad máxima absoluta
    
    # ALTA PRIORIDAD: Movimiento que BLOQUEA al oponente de ganar
    test_board[i][j] = "O"  # Probar movimiento de O
    if check_winner(test_board) == -1:  # Si O ganaría en el siguiente turno
        return 9000  # Prioridad muy alta (debemos bloquear)
    
    # PRIORIDAD MEDIA: Posiciones ESTRATÉGICAS (centro del tablero)
    center = [(1,1), (1,2), (2,1), (2,2)]  # Casillas centrales en 4x4
    if (i, j) in center:
        priority += 100  # El centro es valioso en gato
    
    # PRIORIDAD BAJA: Evaluación de POTENCIAL de líneas afectadas
    directions = [(0,1), (1,0), (1,1), (1,-1)]  # Horizontal, Vertical, Diagonales
    
    for dx, dy in directions:
        line_score = 0
        # Evaluar en ambas direcciones desde la casilla (i,j)
        for sign in [-1, 1]:
            count = 0
            for k in range(1, N):  # Examinar hasta N casillas en esa dirección
                x, y = i + sign * k * dx, j + sign * k * dy
                # Verificar que esté dentro del tablero
                if 0 <= x < N and 0 <= y < N:
                    if board[x][y] == "X":  # Aliado en esa dirección
                        count += 2
                    elif board[x][y] == " ":  # Espacio vacío (potencial)
                        count += 1
                    else:  # Oponente o borde - cortar evaluación
                        break
            line_score += count
        priority += line_score * 10  # Ponderar la evaluación de líneas
    
    return priority

# =============================================================================
# BLOQUE 4: ALGORITMO MINIMAX CON PODA ALFA-BETA
# =============================================================================
def minimax_alfa_beta(board, alpha, beta, maximizing, depth):
    """
    Algoritmo Minimax con poda alfa-beta para encontrar el mejor movimiento.
    
    Parámetros:
    - board: estado actual del tablero
    - alpha: mejor valor que el maximizador puede garantizar (inicialmente -∞)
    - beta: mejor valor que el minimizador puede garantizar (inicialmente +∞)  
    - maximizing: True si es turno del maximizador (X), False para minimizador (O)
    - depth: profundidad actual en el árbol de búsqueda
    """
    
    # 1. VERIFICAR ESTADO TERMINAL (ganador o empate)
    result = check_winner(board)
    if result is not None:
        # Premiar victorias más rápidas (valor más alto por victoria rápida)
        return result * (100 - depth)
    
    # 2. VERIFICAR LÍMITE DE PROFUNDIDAD
    if depth >= MAX_DEPTH:
        # Usar evaluación heurística cuando se alcanza la profundidad máxima
        return evaluate_board(board)
    
    # 3. OBTENER Y ORDENAR MOVIMIENTOS (OPTIMIZACIÓN CRÍTICA)
    moves = []
    for i in range(N):
        for j in range(N):
            if board[i][j] == " ":  # Casilla vacía
                priority = get_move_priority(i, j, board)
                moves.append((priority, i, j))
    
    # ORDENAR por prioridad descendente (mejores movimientos primero)
    moves.sort(reverse=True, key=lambda x: x[0])
    
    # 4. TURNO DEL MAXIMIZADOR (Jugador X - Computadora)
    if maximizing:
        max_eval = float("-inf")  # Inicializar con el peor valor posible
        
        for _, i, j in moves:  # Recorrer movimientos ORDENADOS
            # Probar movimiento
            board[i][j] = "X"
            # Llamada recursiva (turno del minimizador)
            eval = minimax_alfa_beta(board, alpha, beta, False, depth + 1)
            # Deshacer movimiento (backtracking)
            board[i][j] = " "
            
            # Actualizar mejor valor
            max_eval = max(max_eval, eval)
            # Actualizar alpha (mejor valor para maximizador)
            alpha = max(alpha, eval)
            
            # PODA ALFA-BETA: si beta <= alpha, podar rama restante
            if beta <= alpha:
                break  # No evaluar los movimientos restantes
                
        return max_eval
    
    # 5. TURNO DEL MINIMIZADOR (Jugador O - Humano)  
    else:
        min_eval = float("inf")  # Inicializar con el peor valor posible
        
        for _, i, j in moves:  # Recorrer movimientos ORDENADOS
            # Probar movimiento
            board[i][j] = "O"
            # Llamada recursiva (turno del maximizador)
            eval = minimax_alfa_beta(board, alpha, beta, True, depth + 1)
            # Deshacer movimiento (backtracking)
            board[i][j] = " "
            
            # Actualizar mejor valor
            min_eval = min(min_eval, eval)
            # Actualizar beta (mejor valor para minimizador)
            beta = min(beta, eval)
            
            # PODA ALFA-BETA: si beta <= alpha, podar rama restante
            if beta <= alpha:
                break  # No evaluar los movimientos restantes
                
        return min_eval

# =============================================================================
# BLOQUE 5: BÚSQUEDA DEL MEJOR MOVIMIENTO
# =============================================================================
def best_move(board):
    """
    Encuentra el mejor movimiento para la computadora (jugador X).
    Utiliza Minimax con poda alfa-beta y ordenamiento de movimientos.
    """
    best_val = float("-inf")  # Mejor valor encontrado (inicialmente -∞)
    move = (-1, -1)          # Mejor movimiento encontrado
    alpha = float("-inf")    # Límite inferior para poda alfa-beta
    
    # 1. OBTENER Y ORDENAR MOVIMIENTOS
    moves = []
    for i in range(N):
        for j in range(N):
            if board[i][j] == " ":
                priority = get_move_priority(i, j, board)
                moves.append((priority, i, j))
    
    # Ordenar por prioridad descendente (mejores primeros)
    moves.sort(reverse=True, key=lambda x: x[0])
    
    # 2. EVALUAR CADA MOVIMIENTO POSIBLE
    for _, i, j in moves:
        # Probar movimiento
        board[i][j] = "X"
        # Evaluar movimiento usando Minimax
        move_val = minimax_alfa_beta(board, alpha, float("inf"), False, 0)
        # Deshacer movimiento
        board[i][j] = " "
        
        # 3. ACTUALIZAR MEJOR MOVIMIENTO
        if move_val > best_val:
            best_val = move_val
            move = (i, j)
            # Actualizar alpha con el mejor valor actual
            alpha = max(alpha, best_val)
    
    return move

# =============================================================================
# BLOQUE 6: INTERFAZ GRÁFICA (Tkinter)
# =============================================================================

def on_click(i, j):
    """
    Maneja el clic del jugador en una casilla del tablero.
    """
    # Verificar que la casilla esté vacía y el juego no haya terminado
    if board[i][j] == " " and check_winner(board) is None:
        # 1. MOVIMIENTO DEL JUGADOR (O)
        board[i][j] = "O"
        buttons[i][j].config(text="O", state="disabled", bg="lightblue")
        label.config(text="Pensando...")
        root.update()  # Actualizar interfaz inmediatamente
        
        # 2. VERIFICAR SI EL JUGADOR GANÓ
        result = check_winner(board)
        if result is not None:
            show_result(result)
            return
        
        # 3. MOVIMIENTO DE LA COMPUTADORA (X)
        move = best_move(board)  # Encontrar mejor movimiento
        if move != (-1, -1):
            board[move[0]][move[1]] = "X"
            buttons[move[0]][move[1]].config(text="X", state="disabled", bg="lightcoral")
        
        # 4. VERIFICAR RESULTADO DESPUÉS DEL MOVIMIENTO DE LA COMPUTADORA
        result = check_winner(board)
        if result is not None:
            show_result(result)
        else:
            label.config(text="Tu turno (O)")

def show_result(result):
    """
    Muestra el resultado del juego y deshabilita el tablero.
    """
    if result == +1:
        label.config(text="¡La computadora (X) gana!", fg="red")
    elif result == -1:
        label.config(text="¡Tú (O) ganas!", fg="blue")
    else:
        label.config(text="¡Empate!", fg="green")
    
    # Deshabilitar todos los botones
    for i in range(N):
        for j in range(N):
            buttons[i][j].config(state="disabled")

def reset_game():
    """
    Reinicia el juego para empezar de nuevo.
    """
    global board
    # Reiniciar tablero lógico
    board = [[" " for _ in range(N)] for _ in range(N)]
    
    # Reiniciar interfaz gráfica
    for i in range(N):
        for j in range(N):
            buttons[i][j].config(text=" ", state="normal", bg="SystemButtonFace")
    
    # Reiniciar etiqueta de estado
    label.config(text="Tu turno (O)", fg="black")

# =============================================================================
# CONFIGURACIÓN DE LA INTERFAZ GRÁFICA
# =============================================================================

# Crear ventana principal
root = tk.Tk()
root.title(f"Gato {N}x{N} con Minimax y Profundidad Limitada")

# Inicializar tablero lógico y botones gráficos
board = [[" " for _ in range(N)] for _ in range(N)]
buttons = [[None for _ in range(N)] for _ in range(N)]

# Crear botones del tablero
for i in range(N):
    for j in range(N):
        # Crear botón para cada casilla
        buttons[i][j] = tk.Button(
            root, 
            text=" ", 
            font=("Arial", 16, "bold"), 
            width=4, 
            height=2,
            command=lambda i=i, j=j: on_click(i, j)  # Asignar función al clic
        )
        buttons[i][j].grid(row=i, column=j, padx=2, pady=2)

# Etiqueta para mostrar el estado del juego
label = tk.Label(root, text="Tu turno (O)", font=("Arial", 14, "bold"))
label.grid(row=N, column=0, columnspan=N, pady=10)

# Botón para reiniciar el juego
reset_button = tk.Button(
    root, 
    text="Reiniciar Juego", 
    font=("Arial", 12), 
    command=reset_game
)
reset_button.grid(row=N+1, column=0, columnspan=N, pady=5)

# Etiqueta informativa
info_label = tk.Label(
    root, 
    text=f"Profundidad de búsqueda: {MAX_DEPTH} | Tablero: {N}x{N}", 
    font=("Arial", 10)
)
info_label.grid(row=N+2, column=0, columnspan=N, pady=5)

# Iniciar el bucle principal de la interfaz
root.mainloop()