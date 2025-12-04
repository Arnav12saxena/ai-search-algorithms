import random

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
        - list of (new_board, row, new_col) tuples
    """
    n = len(board)
    neighbors = []
    for row in range(n):
        current_col = board[row]
        for new_col in range(n):
            if new_col != current_col:
                new_board = board[:]
                new_board[row] = new_col
                neighbors.append(new_board)
    return neighbors

def hill_climbing(n):
    """
    Perform Hill Climbing search to solve the N-Queens problem.
    
    Args:
        - n: size of the board (N x N)
    
    Returns:
        - list representing the board if solution found, else None
    """
    # Initialize a random board
    board = list(range(n))
    random.shuffle(board)
    
    current_conflicts = calculate_conflicts(board)
    
    while current_conflicts > 0:
        neighbors = get_neighbors(board)
        best_neighbor = None
        best_conflicts = float('inf')
        
        # Find the neighbor with the fewest conflicts
        for neighbor in neighbors:
            neigh_conflicts = calculate_conflicts(neighbor)
            if neigh_conflicts < best_conflicts:
                best_conflicts = neigh_conflicts
                best_neighbor = neighbor
        
        # If no better neighbor, stuck in local minimum
        if best_conflicts >= current_conflicts:
            return None  # Could add random restart here
        
        # Move to the best neighbor
        board = best_neighbor
        current_conflicts = best_conflicts
    
    return board

# Example usage
n = 8  # For 8-Queens
solution = hill_climbing(n)

if solution:
    print("Solution found:", solution)
else:
    print("No solution found (local minimum). Try restarting.")

# Note: Hill Climbing may get stuck, in practice, use random restarts
def hill_climbing_with_restarts(n, max_restarts=100):
    for _ in range(max_restarts):
        solution = hill_climbing(n)
        if solution:
            return solution
    return None

solution_with_restarts = hill_climbing_with_restarts(n)
if solution_with_restarts:
    print("Solution with restarts:", solution_with_restarts)
else:
    print("No solution found after restarts.")