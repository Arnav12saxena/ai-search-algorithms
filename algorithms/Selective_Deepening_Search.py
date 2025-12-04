# Tic-Tac-Toe with Minimax, Alpha-Beta Pruning, and Selective Deepening Search

def print_board(board):
    for row in board:
        print(" | ".join([cell if cell else ' ' for cell in row]))
    print("-" * 5)

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0]:
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col]:
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
        return board[0][2]

    return None

def check_draw(board):
    return all(cell is not None for row in board for cell in row)

def get_available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]

def is_critical_move(board, move, player):
    r, c = move
    temp = [row[:] for row in board]
    temp[r][c] = player

    opponent = 'O' if player == 'X' else 'X'

    lines = [
        # Rows
        [(r, 0), (r, 1), (r, 2)],
        # Columns
        [(0, c), (1, c), (2, c)],
        # Diagonals if applicable
        [(0, 0), (1, 1), (2, 2)] if r == c else [],
        [(0, 2), (1, 1), (2, 0)] if r + c == 2 else []
    ]

    for line in lines:
        if not line: continue
        count_player = sum(1 for rr, cc in line if temp[rr][cc] == player)
        empty = sum(1 for rr, cc in line if temp[rr][cc] is None)
        if count_player == 2 and empty == 1:
            return True

    # Blocking opponent
    for line in lines:
        if not line: continue
        count_op = sum(1 for rr, cc in line if temp[rr][cc] == opponent)
        empty = sum(1 for rr, cc in line if temp[rr][cc] is None)
        if count_op == 2 and empty == 1:
            return True

    return False

def evaluate_board(board):
    winner = check_winner(board)
    if winner == 'X': return 100
    if winner == 'O': return -100
    if check_draw(board): return 0

    score = 0

    lines = [
        [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
        [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
        [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]
    ]

    for line in lines:
        x = sum(1 for r,c in line if board[r][c] == 'X')
        o = sum(1 for r,c in line if board[r][c] == 'O')

        if x > 0 and o == 0:
            score += x
        elif o > 0 and x == 0:
            score -= o

    return score

def minimax_selective(board, depth, max_depth, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == 'X': return 100, None
    if winner == 'O': return -100, None
    if check_draw(board): return 0, None
    if depth >= max_depth:
        return evaluate_board(board), None

    moves = get_available_moves(board)

    # Sort moves so that critical moves go first
    player = 'X' if is_maximizing else 'O'
    moves.sort(key=lambda m: is_critical_move(board, m, player), reverse=True)

    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for r, c in moves:
            new_board = [row[:] for row in board]
            new_board[r][c] = 'X'

            deeper = 2 if is_critical_move(board, (r, c), 'X') else 1

            score, _ = minimax_selective(new_board, depth + deeper, max_depth, False, alpha, beta)

            if score > best_score:
                best_score = score
                best_move = (r, c)

            alpha = max(alpha, score)
            if beta <= alpha: break

        return best_score, best_move

    else:
        best_score = float('inf')
        best_move = None
        for r, c in moves:
            new_board = [row[:] for row in board]
            new_board[r][c] = 'O'

            deeper = 2 if is_critical_move(board, (r, c), 'O') else 1

            score, _ = minimax_selective(new_board, depth + deeper, max_depth, True, alpha, beta)

            if score < best_score:
                best_score = score
                best_move = (r, c)

            beta = min(beta, score)
            if beta <= alpha: break

        return best_score, best_move
