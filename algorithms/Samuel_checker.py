# Tic-Tac-Toe with Samuel-Inspired Minimax and Learning

# Board representation: List of Lists, 3x3 grid
# 'X' for maximizer (AI), 'O' for opponent, None for empty

import random
import copy

def print_board(board):
    for row in board:
        print(" | ".join([cell if cell else ' ' for cell in row]))
    print("-" * 5)

def check_winner(board):
    # Rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0]:
            return row[0]

    # Columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col]:
            return board[0][col]

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
        return board[0][2]

    return None

def check_draw(board):
    return all(cell is not None for row in board for cell in row)

def get_available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]

def evaluate_board(board, weights):
    winner = check_winner(board)
    if winner == 'X': return 100
    if winner == 'O': return -100
    if check_draw(board): return 0

    center_control = 0
    two_in_row = 0
    one_in_row = 0

    # Control of center
    if board[1][1] == 'X': center_control = 1
    elif board[1][1] == 'O': center_control = -1

    # Lines to inspect
    lines = [
        # Rows
        [(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)],
        # Columns
        [(0,0), (1,0), (2,0)], [(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)],
        # Diagonals
        [(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]
    ]

    for line in lines:
        x_count = sum(1 for r, c in line if board[r][c] == 'X')
        o_count = sum(1 for r, c in line if board[r][c] == 'O')
        empty = sum(1 for r, c in line if board[r][c] is None)

        if x_count == 2 and o_count == 0 and empty == 1:
            two_in_row += 1
        elif x_count == 1 and o_count == 0 and empty == 2:
            one_in_row += 1
        elif o_count == 2 and x_count == 0 and empty == 1:
            two_in_row -= 1
        elif o_count == 1 and x_count == 0 and empty == 2:
            one_in_row -= 1

    score = (
        weights[0] * center_control +
        weights[1] * two_in_row +
        weights[2] * one_in_row
    )

    return score

def minimax_alphabeta(board, depth, max_depth, is_maximizing, alpha, beta, weights):
    winner = check_winner(board)
    if winner == 'X': return 100, None
    if winner == 'O': return -100, None
    if check_draw(board): return 0, None
    if depth >= max_depth:
        return evaluate_board(board, weights), None

    moves = get_available_moves(board)

    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for r, c in moves:
            new_board = copy.deepcopy(board)
            new_board[r][c] = 'X'
            score, _ = minimax_alphabeta(new_board, depth + 1, max_depth, False, alpha, beta, weights)

            if score > best_score:
                best_score = score
                best_move = (r, c)

            alpha = max(alpha, score)
            if beta <= alpha:
                break

        return best_score, best_move

    else:
        best_score = float('inf')
        best_move = None
        for r, c in moves:
            new_board = copy.deepcopy(board)
            new_board[r][c] = 'O'
            score, _ = minimax_alphabeta(new_board, depth + 1, max_depth, True, alpha, beta, weights)

            if score < best_score:
                best_score = score
                best_move = (r, c)

            beta = min(beta, score)
            if beta <= alpha:
                break

        return best_score, best_move
