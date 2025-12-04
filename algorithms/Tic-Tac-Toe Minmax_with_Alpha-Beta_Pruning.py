# Tic-Tac-Toe Minimax with Alpha-Beta Pruning

# Board representation: List of lists, 3x3 grid
# 'X' for maximizing, 'O' for minimizing, None for empty

def print_board(board):
    """Print the Tic-Tac-Toe board."""
    for row in board:
        print(' | '.join([cell if cell else ' ' for cell in row]))
        print('- + ' * 2)

def check_winner(board):
    """Check if there's a winner. Returns 'X', 'O', or None."""
    
    for row in board:
        if row[0] == row[1] == row[2] and row[0]:
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col]:
            return board[0][col]
    
    # Check diagonals
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

def minimax_alphabeta(board, is_maximizing, alpha, beta):
    """
    Minimax with Alpha-Beta Pruning to find the best move.
    
    Args:
    - board: current board state
    - is_maximizing: True if maximizing player ('X'), False if minimizing ('O')
    - alpha: best already explored option for maximizer
    - beta: best already explored option for minimizer
    
    Returns:
    - score: int (1 for 'X' win, -1 for 'O' win, 0 for draw)
    - best_move: (row, col) or None
    """
    
    winner = check_winner(board)
    if winner == 'X':
        return 1, None
    if winner == 'O':
        return -1, None
    
    if check_draw(board):
        return 0, None
    
    if is_maximizing:
        max_score = -float('inf')
        best_move = None
        for move in get_available_moves(board):
            i, j = move
            board[i][j] = 'X'
            score, _ = minimax_alphabeta(board, False, alpha, beta)
            board[i][j] = None
            if score > max_score:
                max_score = score
                best_move = move
            alpha = max(alpha, max_score)
            if beta <= alpha:
                break  # Beta cutoff
        return max_score, best_move
    else:
        min_score = float('inf')
        best_move = None
        for move in get_available_moves(board):
            i, j = move
            board[i][j] = 'O'
            score, _ = minimax_alphabeta(board, True, alpha, beta)
            board[i][j] = None
            if score < min_score:
                min_score = score
                best_move = move
            beta = min(beta, min_score)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_score, best_move

def get_best_move(board, player):
    """
    Get the best move for the given player using minimax with alpha-beta pruning.
    
    Args:
    - board: current board
    - player: 'X' or 'O'
    
    Returns:
    - (row, col): best move
    """
    
    is_maximizing = player == 'X'
    _, best_move = minimax_alphabeta(board, is_maximizing, -float('inf'), float('inf'))
    return best_move

# Example: Perfect AI plays against user (starts on both use minimax with alpha-beta [perfect play leads to draw)
board = [[None] * 3 for _ in range(3)]
current_player = 'X'

while True:
    print_board(board)
    if check_winner(board):
        print(f"{check_winner(board)} wins!")
        break
    if check_draw(board):
        print("It's a draw!")
        break
    
    move = get_best_move(board, current_player)
    if move:
        i, j = move
        board[i][j] = current_player
        current_player = 'O' if current_player == 'X' else 'X'
    else:
        print("No moves left!")
        break