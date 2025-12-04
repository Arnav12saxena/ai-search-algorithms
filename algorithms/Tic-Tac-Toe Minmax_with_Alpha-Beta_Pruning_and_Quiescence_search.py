# Tic-Tac-Toe Minimax with Alpha-Beta Pruning and Quiescence Search

# Board representation: list of lists, 3x3 grid
# 'X' for maximizer, 'O' for minimizer, None for empty

def print_board(board):
    """Print the Tic-Tac-Toe board."""
    for row in board:
        print(" | ".join([cell if cell else " " for cell in row]))
        print("-" * 5)

def check_winner(board):
    """Check if there's a winner. Returns 'X', 'O', or None."""
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
    """Check if the board is full (draw)."""
    return all(cell is not None for row in board for cell in row)

def get_available_moves(board):
    """Get list of available moves as (row, col) tuples."""
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]

def is_critical_move(board, move, player):
    """
    Check if a move is critical (creates a two-in-a-row or blocks opponent's win).
    
    Args:
    - board: current board
    - move: (row, col) to check
    - player: 'X' or 'O'
    
    Returns:
    - bool: True if move is critical
    """
    i, j = move
    temp_board = [row[:] for row in board]
    temp_board[i][j] = player
    
    # Check if move creates a two-in-a-row for player
    lines = [
        # Rows
        [(i, 0), (i, 1), (i, 2)],
        # Columns
        [(0, j), (1, j), (2, j)],
        # Diagonals
        [(0, 0), (1, 1), (2, 2)] if i == j else [],
        [(0, 2), (1, 1), (2, 0)] if i + j == 2 else []
    ]
    
    for line in lines:
        if not line:
            continue
        count = sum(1 for r, c in line if temp_board[r][c] == player)
        empty = sum(1 for r, c in line if temp_board[r][c] is None)
        if count == 2 and empty == 1:  # Two pieces, one empty
            return True
    
    # Check if move blocks opponent's win
    opponent = 'O' if player == 'X' else 'X'
    temp_board[i][j] = opponent
    for line in lines:
        if not line:
            continue
        count = sum(1 for r, c in line if temp_board[r][c] == opponent)
        empty = sum(1 for r, c in line if temp_board[r][c] is None)
        if count == 2 and empty == 1:  # Opponent would win
            return True
    
    return False

def evaluate_board(board):
    """
    Evaluate a non-terminal board state.
    Returns a score: positive for 'X' advantage, negative for 'O', 0 for neutral.
    """
    winner = check_winner(board)
    if winner == 'X':
        return 10
    if winner == 'O':
        return -10
    if check_draw(board):
        return 0
    
    # Heuristic: score based on control of winning lines
    score = 0
    lines = [
        # Rows
        [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
        # Columns
        [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
        # Diagonals
        [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
    ]
    
    for line in lines:
        x_count = sum(1 for r, c in line if board[r][c] == 'X')
        o_count = sum(1 for r, c in line if board[r][c] == 'O')
        if x_count == 2 and o_count == 0:  # X closer to winning
            score += 5
        elif o_count == 2 and x_count == 0:  # O closer to winning
            score -= 5
        elif x_count == 1 and o_count == 0:  # X has partial control
            score += 1
        elif o_count == 1 and x_count == 0:  # O has partial control
            score -= 1
    
    return score

def minimax_alphabeta(board, depth, max_depth, is_maximizing, alpha, beta):
    """
    Minimax with Alpha-Beta Pruning.
    
    Args:
    - board: current board
    - depth: current depth
    - max_depth: maximum depth for search
    - is_maximizing: True for 'X', False for 'O'
    - alpha: best option for maximizer
    - beta: best option for minimizer
    
    Returns:
    - score: int (estimated or actual)
    - best_move: (row, col) or None
    """
    winner = check_winner(board)
    if winner == 'X':
        return 100 - depth, None
    if winner == 'O':
        return -100 + depth, None
    if check_draw(board):
        return 0, None
    if depth >= max_depth:
        return evaluate_board(board), None
    
    moves = get_available_moves(board)
    
    # Move ordering: prioritize critical moves
    player = 'X' if is_maximizing else 'O'
    critical_moves = [m for m in moves if is_critical_move(board, m, player)]
    other_moves = [m for m in moves if m not in critical_moves]
    moves = critical_moves + other_moves
    
    if is_maximizing:
        max_eval = float('-inf')
        best_move = None
        for move in moves:
            i, j = move
            board[i][j] = 'X'
            eval_score, _ = minimax_alphabeta(board, depth + 1, max_depth, False, alpha, beta)
            board[i][j] = None
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in moves:
            i, j = move
            board[i][j] = 'O'
            eval_score, _ = minimax_alphabeta(board, depth + 1, max_depth, True, alpha, beta)
            board[i][j] = None
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval, best_move

def play_game():
    """Play a game of Tic-Tac-Toe."""
    board = [[None, None, None] for _ in range(3)]
    print("Tic-Tac-Toe: You are 'O', AI is 'X'")
    print_board(board)
    
    while True:
        # Player move
        while True:
            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter col (0-2): "))
                if board[row][col] is None:
                    board[row][col] = 'O'
                    break
                else:
                    print("Cell already taken!")
            except (ValueError, IndexError):
                print("Invalid input!")
        
        print_board(board)
        winner = check_winner(board)
        if winner:
            print(f"{winner} wins!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        
        # AI move
        print("AI is thinking...")
        _, move = minimax_alphabeta(board, 0, 9, True, float('-inf'), float('inf'))
        if move:
            board[move[0]][move[1]] = 'X'
            print(f"AI plays at {move}")
            print_board(board)
        
        winner = check_winner(board)
        if winner:
            print(f"{winner} wins!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

if __name__ == "__main__":
    play_game()