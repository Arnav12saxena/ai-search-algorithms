# Tic-Tac-Toe with cutoff Search and Alpha-Beta Pruning

# Board representation: list of lists, 3x3 grid
# 'X' for maximizer, 'O' for minimizer, None for empty

def print_board(board):
    """Print the tic-tac-toe board."""
    for row in board:
        print('| ' + ' | '.join([cell if cell else ' ' for cell in row]))
        print('- ' * 5)

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

def evaluate_board(board):
    """
    Evaluate a non-terminal board state.
    Returns a score: positive for 'X' advantage, negative for 'O', 0 for neutral.
    """
    # Heuristic: count potential winning lines (rows, cols, diagonals) for X and O
    score = 0
    
    # Lines to check (rows, columns, diagonals) for X and O
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
        # If line has only X's (and some empty), score positive; only O's -> score negative
        if o_count == 0 and x_count > 0:
            score += x_count
        elif x_count == 0 and o_count > 0:
            score -= o_count
    
    return score

def alpha_beta_pruning(board, depth, is_maximizing, alpha, beta):
    """
    Apply minimax with alpha-beta pruning.
    
    Args:
        - board: current board state
        - depth: current depth in the search tree
        - is_maximizing: True if maximizing ('X'), False if minimizing ('O')
        - alpha: best option for maximizer
        - beta: best option for minimizer
    
    Returns:
        - score: int (estimated or actual)
        - best_move: (row, col) or None
    """
    winner = check_winner(board)
    if winner == 'X':
        return 10, None
    if winner == 'O':
        return -10, None
    if check_draw(board):
        return 0, None
    
    if depth > max_depth:
        return evaluate_board(board), None
    
    if is_maximizing:
        max_score = float('-inf')
        best_move = None
        for move in get_available_moves(board):
            i, j = move
            board[i][j] = 'X'
            score, _ = alpha_beta_pruning(board, depth + 1, False, alpha, beta)
            board[i][j] = None
            if score > max_score:
                max_score = score
                best_move = move
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Beta cutoff
        
        return max_score, best_move
    else:
        min_score = float('inf')
        best_move = None
        for move in get_available_moves(board):
            i, j = move
            board[i][j] = 'O'
            score, _ = alpha_beta_pruning(board, depth + 1, True, alpha, beta)
            board[i][j] = None
            if score < min_score:
                min_score = score
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break  # Alpha cutoff
        
        return min_score, best_move

def get_best_move(board, player, max_depth=3):
    """
    Get the best move for the given player using minimax with alpha-beta pruning.
    
    Args:
        - board: current board
        - player: 'X' or 'O'
        - max_depth: depth limit for search
    
    Returns:
        - (row, col): best move
    """
    is_maximizing = player == 'X'
    _, best_move = alpha_beta_pruning(board, 0, is_maximizing, float('-inf'), float('-inf'))
    return best_move

# Example usage: Play a game where 'X' starts and both use minimax with alpha-beta pruning
board = [[None, None, None] for _ in range(3)]
current_player = 'X'
max_depth = 9  # Full search for 3x3 board

while True:
    print_board(board)
    if check_winner(board):
        print(f"[check_winner(board)] wins!")
        break
    if check_draw(board):
        print("It's a draw!")
        break
    
    move = get_best_move(board, current_player, max_depth)
    if move:
        i, j = move
        board[i][j] = current_player
        current_player = 'O' if current_player == 'X' else 'X'
    else:
        print("No moves left!")
        break