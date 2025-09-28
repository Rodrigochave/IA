import tkinter as tk

N = 4  # tamaño del tablero 4x4
MAX_DEPTH = 3  # Profundidad máxima de búsqueda (ajustable)

def check_winner(board):
    # Verificar filas
    for i in range(N):
        if all(board[i][j] == "X" for j in range(N)):
            return +1
        if all(board[i][j] == "O" for j in range(N)):
            return -1
    
    # Verificar columnas
    for j in range(N):
        if all(board[i][j] == "X" for i in range(N)):
            return +1
        if all(board[i][j] == "O" for i in range(N)):
            return -1
    
    # Verificar diagonales principales
    if all(board[i][i] == "X" for i in range(N)):
        return +1
    if all(board[i][i] == "O" for i in range(N)):
        return -1
    
    # Verificar diagonales secundarias
    if all(board[i][N-1-i] == "X" for i in range(N)):
        return +1
    if all(board[i][N-1-i] == "O" for i in range(N)):
        return -1
    
    # Verificar empate
    if all(board[i][j] != " " for i in range(N) for j in range(N)):
        return 0
    
    return None

def evaluate_board(board):
    """
    Función de evaluación heurística para el tablero 4x4.
    Asigna un valor numérico a la posición actual.
    """
    score = 0
    
    # Líneas a verificar: filas, columnas y diagonales
    lines = []
    
    # Filas
    for i in range(N):
        lines.append([(i, j) for j in range(N)])
    
    # Columnas
    for j in range(N):
        lines.append([(i, j) for i in range(N)])
    
    # Diagonales principales
    lines.append([(i, i) for i in range(N)])
    lines.append([(i, N-1-i) for i in range(N)])
    
    # Evaluar cada línea
    for line in lines:
        x_count = sum(1 for i, j in line if board[i][j] == "X")
        o_count = sum(1 for i, j in line if board[i][j] == "O")
        
        # Si la línea tiene potencial para X (sin O)
        if o_count == 0:
            if x_count == 3:
                score += 100  # Casi ganadora para X
            elif x_count == 2:
                score += 10   # Buena posición para X
            elif x_count == 1:
                score += 1    # Posición inicial para X
        
        # Si la línea tiene potencial para O (sin X)
        elif x_count == 0:
            if o_count == 3:
                score -= 100  # Casi ganadora para O
            elif o_count == 2:
                score -= 10   # Buena posición para O
            elif o_count == 1:
                score -= 1    # Posición inicial para O
    
    # Priorizar el centro del tablero (especialmente en 4x4)
    center_positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
    for i, j in center_positions:
        if board[i][j] == "X":
            score += 3
        elif board[i][j] == "O":
            score -= 3
    
    return score

def minimax_alfa_beta(board, alpha, beta, maximizing, depth):
    """
    Minimax con poda alfa-beta y profundidad limitada.
    """
    result = check_winner(board)
    if result is not None:
        return result * (100 - depth)  # Premiar victorias rápidas
    
    # Si alcanzamos la profundidad máxima, usar evaluación heurística
    if depth >= MAX_DEPTH:
        return evaluate_board(board)
    
    if maximizing:  # Turno de la computadora (X)
        max_eval = float("-inf")
        for i in range(N):
            for j in range(N):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    eval = minimax_alfa_beta(board, alpha, beta, False, depth + 1)
                    board[i][j] = " "
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return max_eval
    else:  # Turno del jugador (O)
        min_eval = float("inf")
        for i in range(N):
            for j in range(N):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    eval = minimax_alfa_beta(board, alpha, beta, True, depth + 1)
                    board[i][j] = " "
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return min_eval

def best_move(board):
    """
    Encuentra el mejor movimiento para la computadora.
    """
    best_val = float("-inf")
    move = (-1, -1)
    
    # Ordenar movimientos para mejorar la poda alfa-beta
    # Priorizar movimientos centrales y esquinas
    moves = []
    for i in range(N):
        for j in range(N):
            if board[i][j] == " ":
                # Dar prioridad a movimientos centrales
                priority = abs(i - N//2) + abs(j - N//2)
                moves.append((priority, i, j))
    
    # Ordenar por prioridad (movimientos más centrales primero)
    moves.sort()
    
    for _, i, j in moves:
        if board[i][j] == " ":
            board[i][j] = "X"
            move_val = minimax_alfa_beta(board, float("-inf"), float("inf"), False, 0)
            board[i][j] = " "
            if move_val > best_val:
                best_val = move_val
                move = (i, j)
    
    return move

# ----------------- Interfaz gráfica -----------------

def on_click(i, j):
    if board[i][j] == " " and check_winner(board) is None:
        # Movimiento del jugador (O)
        board[i][j] = "O"
        buttons[i][j].config(text="O", state="disabled", bg="lightblue")
        label.config(text="Pensando...")
        root.update()  # Actualizar la interfaz inmediatamente

        result = check_winner(board)
        if result is not None:
            show_result(result)
            return

        # Movimiento de la computadora (X)
        move = best_move(board)
        if move != (-1, -1):
            board[move[0]][move[1]] = "X"
            buttons[move[0]][move[1]].config(text="X", state="disabled", bg="lightcoral")

        result = check_winner(board)
        if result is not None:
            show_result(result)
        else:
            label.config(text="Tu turno (O)")

def show_result(result):
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
    global board
    board = [[" " for _ in range(N)] for _ in range(N)]
    
    for i in range(N):
        for j in range(N):
            buttons[i][j].config(text=" ", state="normal", bg="SystemButtonFace")
    
    label.config(text="Tu turno (O)", fg="black")

# Crear la interfaz
root = tk.Tk()
root.title(f"Gato {N}x{N} con Minimax y Profundidad Limitada")

board = [[" " for _ in range(N)] for _ in range(N)]
buttons = [[None for _ in range(N)] for _ in range(N)]

# Crear botones del tablero
for i in range(N):
    for j in range(N):
        buttons[i][j] = tk.Button(
            root, 
            text=" ", 
            font=("Arial", 16, "bold"), 
            width=4, 
            height=2,
            command=lambda i=i, j=j: on_click(i, j)
        )
        buttons[i][j].grid(row=i, column=j, padx=2, pady=2)

# Etiqueta de estado
label = tk.Label(root, text="Tu turno (O)", font=("Arial", 14, "bold"))
label.grid(row=N, column=0, columnspan=N, pady=10)

# Botón de reinicio
reset_button = tk.Button(
    root, 
    text="Reiniciar Juego", 
    font=("Arial", 12), 
    command=reset_game
)
reset_button.grid(row=N+1, column=0, columnspan=N, pady=5)

# Información sobre la configuración
info_label = tk.Label(
    root, 
    text=f"Profundidad de búsqueda: {MAX_DEPTH} | Tablero: {N}x{N}", 
    font=("Arial", 10)
)
info_label.grid(row=N+2, column=0, columnspan=N, pady=5)

root.mainloop()