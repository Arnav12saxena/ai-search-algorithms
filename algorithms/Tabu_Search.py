import random
from collections import deque

def calculate_conflicts(board):
    """
    Calculate the number of conflicts (attacking pairs) in the current board configuration.
    
    Args:
    - board: list where index is row, value is column of the queen
    
    Returns:
    - int: number of conflicting pairs
    """
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Same column or diagonal
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                conflicts += 1
    return conflicts

def get_neighbors(board):
    """
    Generate all possible neighbors by moving one queen to a different column in its row.
    
    Args:
    - board: current board configuration
    
    Returns:
    - List of (new_board, row, new_col) tuples
    """
    n = len(board)
    neighbors = []
    for row in range(n):
        current_col = board[row]
        for new_col in range(n):
            if new_col != current_col:
                new_board = board[:]
                new_board[row] = new_col
                neighbors.append((new_board, row, new_col))
    return neighbors

def tabu_search(n, max_iterations=1000, tabu_size=50):
    """
    Perform Tabu Search to solve the N-Queens problem.
    
    Args:
    - n: size of the board (N x N)
    - max_iterations: maximum number of iterations
    - tabu_size: size of the tabu list to prevent cycling
    
    Returns:
    - list representing the board if solution found, else None
    """
    
    # Initialize a random board
    current_board = list(range(n))
    random.shuffle(current_board)
    current_conflicts = calculate_conflicts(current_board)
    
    best_board = current_board[:]
    best_conflicts = current_conflicts
    
    # Tabu list to store recent moves (row, col) to avoid
    tabu_list = deque(maxlen=tabu_size)
    
    iteration = 0
    while iteration < max_iterations:
        neighbors = get_neighbors(current_board)
        best_neighbor = None
        best_neighbor_conflicts = float('inf')
        best_move = None
        
        # Find the best non-tabu neighbor
        for neighbor, row, new_col in neighbors:
            conflicts = calculate_conflicts(neighbor)
            if conflicts < best_neighbor_conflicts and (row, new_col) not in tabu_list:
                best_neighbor = neighbor
                best_neighbor_conflicts = conflicts
                best_move = (row, new_col)
        
        # If no valid neighbor found, break (stuck)
        if best_neighbor is None:
            break
        
        # Update current solution
        current_board = best_neighbor
        current_conflicts = best_neighbor_conflicts
        tabu_list.append(best_move)
        
        # Update best solution if current is better
        if current_conflicts < best_conflicts:
            best_board = current_board[:]
            best_conflicts = current_conflicts
        
        # Stop if a solution is found
        if best_conflicts == 0:
            return best_board
        
        iteration += 1
    
    return best_board if best_conflicts == 0 else None

# Example usage
n = 8  # for 8-Queens
solution = tabu_search(n)

if solution:
    print("Solution found:", solution)
else:
    print("No solution found.")