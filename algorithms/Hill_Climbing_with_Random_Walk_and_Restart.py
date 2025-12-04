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
        - list of new board configurations
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

def hill_climbing_with_random_walk_and_restart(n, random_walk_prob=0.1, max_restarts=100, max_steps=1000):
    """
    Perform Hill Climbing with random walk and random restarts to solve the N-Queens problem.
    
    Args:
        - n: size of the board (N x N)
        - random_walk_prob: probability of making a random move instead of the best move
        - max_restarts: maximum number of random restarts
        - max_steps: maximum steps per restart before giving up
    
    Returns:
        - list representing the board if solution found, else None
    """
    for restart in range(max_restarts):
        # Initialize a random board
        current_board = list(range(n))
        random.shuffle(current_board)
        current_conflicts = calculate_conflicts(current_board)
        
        step = 0
        while current_conflicts > 0 and step < max_steps:
            neighbors = get_neighbors(current_board)
            if not neighbors:
                break
            
            # Random walk: with probability random_walk_prob, pick a random neighbor
            if random.random() < random_walk_prob:
                current_board = random.choice(neighbors)
                current_conflicts = calculate_conflicts(current_board)
            else:
                # Standard Hill Climbing: pick the neighbor with the fewest conflicts
                best_neighbor = None
                best_conflicts = float('inf')
                
                for neighbor in neighbors:
                    neigh_conflicts = calculate_conflicts(neighbor)
                    if neigh_conflicts < best_conflicts:
                        best_conflicts = neigh_conflicts
                        best_neighbor = neighbor
                
                # If no better neighbor, break (stuck in local minimum)
                if best_conflicts >= current_conflicts:
                    break
                
                # Move to the best neighbor
                current_board = best_neighbor
                current_conflicts = best_conflicts
            
            step += 1
        
        # If a solution is found (no conflicts), return it
        if current_conflicts == 0:
            return current_board
    
    return None

# Example usage
n = 8  # For 8-Queens
solution = hill_climbing_with_random_walk_and_restart(n)

if solution:
    print("Solution found:", solution)
else:
    print("No solution found (local minimum). Try restarting.")