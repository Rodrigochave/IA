#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <math.h>
#include <string.h>

#define N 4
#define MAX_DEPTH 3
#define EMPTY ' '
#define PLAYER 'O'
#define COMPUTER 'X'

// Estructura para representar un movimiento
typedef struct {
    int i, j;
} Move;

// Estructura para movimientos con prioridad
typedef struct {
    int priority;
    int i, j;
} PriorityMove;

// Prototipos de funciones
int check_winner(char board[N][N]);
int evaluate_line(int line[N][2], char board[N][N]);
int evaluate_board(char board[N][N]);
int get_move_priority(int i, int j, char board[N][N]);
int minimax_alfa_beta(char board[N][N], int alpha, int beta, int maximizing, int depth);
Move best_move(char board[N][N]);
void print_board(char board[N][N]);
void initialize_board(char board[N][N]);
int get_human_move(char board[N][N]);
int is_board_full(char board[N][N]);

// =============================================================================
// FUNCIÓN PRINCIPAL - CORREGIDA
// =============================================================================
int main() {
    char board[N][N];
    int game_over = 0;
    int result;
    Move computer_move;
    
    printf("=== GATO %dx%d con MINIMAX y PODA ALFA-BETA ===\n", N, N);
    printf("Tu eres: %c | Computadora: %c\n", PLAYER, COMPUTER);
    printf("Profundidad de busqueda: %d\n\n", MAX_DEPTH);
    
    initialize_board(board);
    
    while (!game_over) {
        // Turno del jugador humano
        print_board(board);
        
        // Verificar estado del juego antes del movimiento
        result = check_winner(board);
        if (result != 0 || is_board_full(board)) {
            break;
        }
        
        printf("Tu turno (%c). Ingresa fila y columna (ej: 1 2): ", PLAYER);
        if (get_human_move(board) == -1) {
            printf("Movimiento invalido. Intenta de nuevo.\n");
            continue;
        }
        
        // Verificar estado después del movimiento humano
        result = check_winner(board);
        if (result != 0) {
            print_board(board);
            if (result == -1) {
                printf("¡Felicidades! Ganaste.\n");
            } else if (result == 1) {
                printf("¡La computadora gana!\n");
            }
            game_over = 1;
            break;
        }
        
        // Verificar empate después del movimiento humano
        if (is_board_full(board)) {
            print_board(board);
            printf("¡Empate!\n");
            game_over = 1;
            break;
        }
        
        // Turno de la computadora
        printf("Computadora pensando...\n");
        computer_move = best_move(board);
        
        if (computer_move.i != -1 && computer_move.j != -1) {
            board[computer_move.i][computer_move.j] = COMPUTER;
            printf("Computadora juega en: (%d, %d)\n", 
                   computer_move.i + 1, computer_move.j + 1);
        }
        
        // Verificar estado después del movimiento de la computadora
        result = check_winner(board);
        if (result != 0) {
            print_board(board);
            if (result == 1) {
                printf("¡La computadora gana!\n");
            } else if (result == -1) {
                printf("¡Felicidades! Ganaste.\n");
            }
            game_over = 1;
            break;
        }
        
        // Verificar empate después del movimiento de la computadora
        if (is_board_full(board)) {
            print_board(board);
            printf("¡Empate!\n");
            game_over = 1;
            break;
        }
    }
    
    // Verificación final por si salimos del bucle sin detectar empate
    if (!game_over) {
        result = check_winner(board);
        if (result == 0 && is_board_full(board)) {
            print_board(board);
            printf("¡Empate!\n");
        }
    }
    
    return 0;
}

// =============================================================================
// FUNCIÓN PARA VERIFICAR SI EL TABLERO ESTÁ LLENO
// =============================================================================
int is_board_full(char board[N][N]) {
    int i, j;
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            if (board[i][j] == EMPTY) {
                return 0; // No está lleno
            }
        }
    }
    return 1; // Está lleno
}

// =============================================================================
// INICIALIZACIÓN DEL TABLERO
// =============================================================================
void initialize_board(char board[N][N]) {
    int i, j;
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            board[i][j] = EMPTY;
        }
    }
}

// =============================================================================
// IMPRIMIR TABLERO
// =============================================================================
void print_board(char board[N][N]) {
    int i, j;
    printf("\n");
    printf("   ");
    for (j = 0; j < N; j++) {
        printf(" %d  ", j + 1);
    }
    printf("\n");
    
    for (i = 0; i < N; i++) {
        printf("%d |", i + 1);
        for (j = 0; j < N; j++) {
            printf(" %c |", board[i][j]);
        }
        printf("\n");
        
        if (i < N - 1) {
            printf("  +");
            for (j = 0; j < N; j++) {
                printf("---+");
            }
            printf("\n");
        }
    }
    printf("\n");
}

// =============================================================================
// DETECCIÓN DE GANADOR - SIMPLIFICADA Y CORREGIDA
// =============================================================================
int check_winner(char board[N][N]) {
    int i, j;
    
    // Verificar filas
    for (i = 0; i < N; i++) {
        int row_x = 1, row_o = 1;
        for (j = 0; j < N; j++) {
            if (board[i][j] != COMPUTER) row_x = 0;
            if (board[i][j] != PLAYER) row_o = 0;
        }
        if (row_x) return 1;
        if (row_o) return -1;
    }
    
    // Verificar columnas
    for (j = 0; j < N; j++) {
        int col_x = 1, col_o = 1;
        for (i = 0; i < N; i++) {
            if (board[i][j] != COMPUTER) col_x = 0;
            if (board[i][j] != PLAYER) col_o = 0;
        }
        if (col_x) return 1;
        if (col_o) return -1;
    }
    
    // Verificar diagonal principal
    int diag1_x = 1, diag1_o = 1;
    for (i = 0; i < N; i++) {
        if (board[i][i] != COMPUTER) diag1_x = 0;
        if (board[i][i] != PLAYER) diag1_o = 0;
    }
    if (diag1_x) return 1;
    if (diag1_o) return -1;
    
    // Verificar diagonal secundaria
    int diag2_x = 1, diag2_o = 1;
    for (i = 0; i < N; i++) {
        if (board[i][N-1-i] != COMPUTER) diag2_x = 0;
        if (board[i][N-1-i] != PLAYER) diag2_o = 0;
    }
    if (diag2_x) return 1;
    if (diag2_o) return -1;
    
    return 0; // No hay ganador todavía
}

// =============================================================================
// EVALUACIÓN HEURÍSTICA
// =============================================================================
int evaluate_line(int line[N][2], char board[N][N]) {
    int k;
    int x_count = 0, o_count = 0;
    
    for (k = 0; k < N; k++) {
        int i = line[k][0], j = line[k][1];
        if (board[i][j] == COMPUTER) x_count++;
        else if (board[i][j] == PLAYER) o_count++;
    }
    
    if (o_count == 0 && x_count > 0) {
        return (int)pow(10, x_count);
    } else if (x_count == 0 && o_count > 0) {
        return -(int)pow(10, o_count);
    }
    
    return 0;
}

int evaluate_board(char board[N][N]) {
    int i, j, k;
    int score = 0;
    int row[N][2], col[N][2];
    int diag1[N][2], diag2[N][2];
    
    // Evaluar filas y columnas
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            row[j][0] = i; row[j][1] = j;  // Fila i
            col[j][0] = j; col[j][1] = i;  // Columna i
        }
        
        score += evaluate_line(row, board);
        score += evaluate_line(col, board);
    }
    
    // Evaluar diagonales
    for (i = 0; i < N; i++) {
        diag1[i][0] = i; diag1[i][1] = i;           // Diagonal principal
        diag2[i][0] = i; diag2[i][1] = N-1-i;       // Diagonal secundaria
    }
    
    score += evaluate_line(diag1, board);
    score += evaluate_line(diag2, board);
    
    return score;
}

// =============================================================================
// CÁLCULO DE PRIORIDAD DE MOVIMIENTOS
// =============================================================================
int get_move_priority(int i, int j, char board[N][N]) {
    int k, d, sign, x, y, dx, dy, count, line_score;
    int priority = 0;
    char test_board[N][N];
    int center_positions[4][2] = {{1,1}, {1,2}, {2,1}, {2,2}};
    int directions[4][2] = {{0,1}, {1,0}, {1,1}, {1,-1}};
    
    // Verificar movimiento ganador
    memcpy(test_board, board, sizeof(test_board));
    test_board[i][j] = COMPUTER;
    if (check_winner(test_board) == 1) return 10000;
    
    // Verificar si bloquea al oponente
    memcpy(test_board, board, sizeof(test_board));
    test_board[i][j] = PLAYER;
    if (check_winner(test_board) == -1) return 9000;
    
    // Posiciones centrales (estratégicas)
    for (k = 0; k < 4; k++) {
        if (i == center_positions[k][0] && j == center_positions[k][1]) {
            priority += 100;
            break;
        }
    }
    
    // Evaluar direcciones adyacentes
    for (d = 0; d < 4; d++) {
        dx = directions[d][0]; 
        dy = directions[d][1];
        line_score = 0;
        
        for (sign = -1; sign <= 1; sign += 2) {
            count = 0;
            for (k = 1; k < N; k++) {
                x = i + sign * k * dx;
                y = j + sign * k * dy;
                
                if (x >= 0 && x < N && y >= 0 && y < N) {
                    if (board[x][y] == COMPUTER) count += 2;
                    else if (board[x][y] == EMPTY) count += 1;
                    else break;
                } else {
                    break;
                }
            }
            line_score += count;
        }
        priority += line_score * 10;
    }
    
    return priority;
}

// =============================================================================
// ALGORITMO MINIMAX CON PODA ALFA-BETA
// =============================================================================
int minimax_alfa_beta(char board[N][N], int alpha, int beta, int maximizing, int depth) {
    int i, j, k, m;
    int eval, max_eval, min_eval;
    int result = check_winner(board);
    PriorityMove moves[N*N];
    int move_count = 0;
    
    // Si hay un ganador o empate, retornar evaluación
    if (result != 0) {
        return result * (100 - depth);
    }
    
    if (is_board_full(board)) {
        return 0; // Empate
    }
    
    if (depth >= MAX_DEPTH) {
        return evaluate_board(board);
    }
    
    // Obtener y ordenar movimientos
    move_count = 0;
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            if (board[i][j] == EMPTY) {
                moves[move_count].priority = get_move_priority(i, j, board);
                moves[move_count].i = i;
                moves[move_count].j = j;
                move_count++;
            }
        }
    }
    
    // Ordenar movimientos por prioridad (bubble sort simple)
    for (k = 0; k < move_count - 1; k++) {
        for (m = 0; m < move_count - k - 1; m++) {
            if (moves[m].priority < moves[m+1].priority) {
                PriorityMove temp = moves[m];
                moves[m] = moves[m+1];
                moves[m+1] = temp;
            }
        }
    }
    
    if (maximizing) {
        max_eval = INT_MIN;
        
        for (k = 0; k < move_count; k++) {
            i = moves[k].i; 
            j = moves[k].j;
            board[i][j] = COMPUTER;
            
            eval = minimax_alfa_beta(board, alpha, beta, 0, depth + 1);
            board[i][j] = EMPTY;
            
            if (eval > max_eval) max_eval = eval;
            if (eval > alpha) alpha = eval;
            if (beta <= alpha) break;
        }
        return max_eval;
    } else {
        min_eval = INT_MAX;
        
        for (k = 0; k < move_count; k++) {
            i = moves[k].i; 
            j = moves[k].j;
            board[i][j] = PLAYER;
            
            eval = minimax_alfa_beta(board, alpha, beta, 1, depth + 1);
            board[i][j] = EMPTY;
            
            if (eval < min_eval) min_eval = eval;
            if (eval < beta) beta = eval;
            if (beta <= alpha) break;
        }
        return min_eval;
    }
}

// =============================================================================
// ENCONTRAR MEJOR MOVIMIENTO
// =============================================================================
Move best_move(char board[N][N]) {
    int i, j, k, m;
    int move_val, best_val;
    int alpha;
    Move best_move;
    PriorityMove moves[N*N];
    int move_count = 0;
    
    best_move.i = -1; 
    best_move.j = -1;
    best_val = INT_MIN;
    alpha = INT_MIN;
    
    // Obtener todos los movimientos posibles
    move_count = 0;
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            if (board[i][j] == EMPTY) {
                moves[move_count].priority = get_move_priority(i, j, board);
                moves[move_count].i = i;
                moves[move_count].j = j;
                move_count++;
            }
        }
    }
    
    // Ordenar movimientos
    for (k = 0; k < move_count - 1; k++) {
        for (m = 0; m < move_count - k - 1; m++) {
            if (moves[m].priority < moves[m+1].priority) {
                PriorityMove temp = moves[m];
                moves[m] = moves[m+1];
                moves[m+1] = temp;
            }
        }
    }
    
    // Evaluar cada movimiento
    for (k = 0; k < move_count; k++) {
        i = moves[k].i; 
        j = moves[k].j;
        board[i][j] = COMPUTER;
        
        move_val = minimax_alfa_beta(board, alpha, INT_MAX, 0, 0);
        board[i][j] = EMPTY;
        
        if (move_val > best_val) {
            best_val = move_val;
            best_move.i = i;
            best_move.j = j;
            alpha = move_val;
        }
    }
    
    return best_move;
}

// =============================================================================
// ENTRADA DEL JUGADOR HUMANO
// =============================================================================
int get_human_move(char board[N][N]) {
    int row, col;
    int c;
    
    if (scanf("%d %d", &row, &col) != 2) {
        // Limpiar buffer de entrada en caso de error
        while ((c = getchar()) != '\n' && c != EOF);
        return -1;
    }
    
    // Convertir a índices base 0 y validar
    row--; col--;
    
    if (row < 0 || row >= N || col < 0 || col >= N || board[row][col] != EMPTY) {
        return -1;
    }
    
    board[row][col] = PLAYER;
    return 0;
}
