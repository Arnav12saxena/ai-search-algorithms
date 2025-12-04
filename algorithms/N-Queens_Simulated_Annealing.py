import random
import math

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

def get_random_neighbor(board):
    """
    Generate a random neighbor by moving one queen to a different column in its row.
    
    Args:
    - board: current board configuration
    
    Returns:
    - new board configuration
    """
    n = len(board)
    new_board = board[:]
    row = random.randint(0, n - 1)
    current_col = new_board[row]
    new_col = random.choice([col for col in range(n) if col is not current_col])
    new_board[row] = new_col
    return new_board

def simulated_annealing(n, initial_temp=1000, cooling_rate=0.95, max_iterations=10000):
    """
    Perform Simulated Annealing to solve the N-Queens problem.
    
    Args:
    - n: size of the board (N x N)
    - initial_temp: starting temperature
    - cooling_rate: factor by which temperature decreases each iteration
    - max_iterations: maximum number of iterations
    
    Returns:
    - list representing the board if solution found, else None
    """
    
    # Initialize a random board
    current_board = list(range(n))
    random.shuffle(current_board)
    current_conflicts = calculate_conflicts(current_board)
    
    best_board = current_board[:]
    best_conflicts = current_conflicts
    
    temperature = initial_temp
    iteration = 0
    
    while temperature > 0.1 and iteration < max_iterations:
        # Generate a random neighbor
        neighbor = get_random_neighbor(current_board)
        neighbor_conflicts = calculate_conflicts(neighbor)
        
        # Accept the neighbor if better or with a probability based on temperature
        delta = neighbor_conflicts - current_conflicts
        if delta <= 0 or random.random() < math.exp(-delta / temperature):
            current_board = neighbor
            current_conflicts = neighbor_conflicts
            
            # Update best solution if current is better
            if current_conflicts < best_conflicts:
                best_board = current_board[:]
                best_conflicts = current_conflicts
        
        # Stop if a solution is found
        if best_conflicts == 0:
            return best_board
        
        # Cool down the temperature
        temperature *= cooling_rate
        iteration += 1
    
    return best_board if best_conflicts == 0 else None

# Example usage
n = 8  # for 8-Queens
solution = simulated_annealing(n)

if solution:
    print("Solution found:", solution)
else:
    print("No solution found.")