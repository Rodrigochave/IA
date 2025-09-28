def minimax_alfa_beta(board, alpha, beta, maximizing):
    result = check_winner(board)
    if result is not None:
        return result

    if maximizing:  # Turno de la computadora (X)
        max_eval = float("-inf")
        for i in range(N):
            for j in range(N):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    eval = minimax_alfa_beta(board, alpha, beta, False)
                    board[i][j] = " "
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:  # poda
                        break
        return max_eval
    else:  # Turno del jugador (O)
        min_eval = float("inf")
        for i in range(N):
            for j in range(N):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    eval = minimax_alfa_beta(board, alpha, beta, True)
                    board[i][j] = " "
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:  # poda
                        break
        return min_eval


def best_move(board):
    best_val = float("-inf")
    move = (-1, -1)
    for i in range(N):
        for j in range(N):
            if board[i][j] == " ":
                board[i][j] = "X"
                move_val = minimax_alfa_beta(board, float("-inf"), float("inf"), False)
                board[i][j] = " "
                if move_val > best_val:
                    best_val = move_val
                    move = (i, j)
    return move
