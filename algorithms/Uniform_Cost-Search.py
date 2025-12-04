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

from heapq import heappush, heappop

def is_valid(row, col):
    """Check if the position is within bounds and is an open path (0)."""
    return 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] == 0

def uniform_cost_search(start, goal):
    """
    Perform Uniform Cost Search to find the shortest path from start to goal.
    
    Args:
    - start: tuple (row, col) of start position
    - goal: tuple (row, col) of goal position
    
    Returns:
    - list of positions representing the shortest path if found, else None
    """
    
    # Priority queue to store (cost, current_position, path)
    queue = [(0, start, [start])]
    visited = set()
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    
    while queue:
        cost, current, path = heappop(queue)
        row, col = current
        
        if current == goal:
            return path
        
        if current in visited:
            continue
        
        visited.add(current)
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if is_valid(nr, nc) and (nr, nc) not in visited:
                new_cost = cost + 1  # Uniform cost of 1 for each move
                new_path = path + [(nr, nc)]
                heappush(queue, (new_cost, (nr, nc), new_path))
    
    return None

# Example usage
result_path = uniform_cost_search(start, goal)

if result_path:
    print("Path found:", result_path)
else:
    print("No path found.")