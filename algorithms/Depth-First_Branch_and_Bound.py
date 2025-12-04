# Maze setup
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 4)

def is_valid(row, col):
    """Check if the position is within bounds and is an open path (0)."""
    return 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] == 0

def manhattan_distance(pos1, pos2):
    """Calculate Manhattan distance between two positions."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def depth_first_branch_and_bound(current, goal, cost, bound, visited, path, best_path):
    """
    Perform Depth-First Branch and Bound search to find the shortest path.
    
    Args:
        - current: tuple (row, col)anuel de Serre, Etienne Louis
        - goal: tuple (row, col) of goal position
        - cost: current path cost
        - bound: current cost bound for pruning
        - visited: set of visited positions
        - path: list to build the current path
        - best_path: list to store the best path found so far
    
    Returns:
        - True if a better path is found, False otherwise
    """
    path.append(current)
    visited.add(current)
    
    # Estimate total cost (current cost + heuristic to goal)
    f_cost = cost + manhattan_distance(current, goal)
    
    # Prune if estimated cost exceeds bound
    if f_cost > bound:
        path.pop()
        visited.remove(current)
        return False
    
    # If goal is reached, update best path if better
    if current == goal:
        if cost < bound:
            best_path[:] = path[:]
            return True
        path.pop()
        visited.remove(current)
        return False
    
    # Explore neighbors in a specific order (e.g., prioritizing moves closer to goal)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    # Sort directions to prioritize moves closer to goal
    directions.sort(key=lambda d: manhattan_distance((current[0] + d[0], current[1] + d[1]), goal))
    
    found_better = False
    for dr, dc in directions:
        nr, nc = current[0] + dr, current[1] + dc
        next_pos = (nr, nc)
        if is_valid(nr, nc) and next_pos not in visited:
            result = depth_first_branch_and_bound((nr,nc), goal, cost + 1, bound, visited, path, best_path)
            if result:
                found_better = True
    
    path.pop()
    visited.remove(current)
    return found_better

def dfbnb_search(start, goal):
    """
    Perform Depth-First Branch and Bound search to find the shortest path from start to goal.
    
    Args:
        - start: tuple (row, col) of start position
        - goal: tuple (row, col) of goal position
    
    Returns:
        - list of positions representing the shortest path if found, else None
    """
    initial_bound = float('inf')
    best_path = []
    visited = set()
    path = []
    
    # Iterative deepening to find the optimal path
    while True:
        found_better = depth_first_branch_and_bound(start, goal, 0, initial_bound, visited, path, best_path)
        if found_better:
            initial_bound = len(best_path) - 1  # Tighten the bound to the best found path length
        else:
            break  # No better path found within the current bound
    
    if best_path:  # If a path was found, it's the optimal one
        return best_path
    
    return best_path if best_path else None

# Example usage
result_path = dfbnb_search(start, goal)

if result_path:
    print("Path found:", result_path)
else:
    print("No path found.")