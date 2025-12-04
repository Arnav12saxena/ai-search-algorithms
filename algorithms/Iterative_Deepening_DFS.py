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

def depth_limited_search(current, goal, depth, visited, path):
    """
    Perform depth-limited search for a given depth limit.
    
    Args:
        - current: tuple (row, col) of current position
        - goal: tuple (row, col) of goal position
        - depth: current remaining depth limit
        - visited: set of visited positions to avoid cycles
        - path: list to build the path
    
    Returns:
        - list of positions if path found, else None
    """
    row, col = current
    path.append(current)
    
    if current == goal:
        return path[:]  # Return a copy of the path
    
    if depth <= 0:
        path.pop()
        return None
    
    visited.add(current)
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if is_valid(nr, nc) and (nr, nc) not in visited:
            result = depth_limited_search((nr, nc), goal, depth - 1, visited, path)
            if result:
                return result
    
    path.pop()
    visited.remove(current)  # Backtrack
    return None

def iterative_deepening_dfs(start, goal, max_depth):
    """
    Perform Iterative Deepening Depth-First Search to find a path from start to goal.
    
    Args:
        - start: tuple (row, col) of start position
        - goal: tuple (row, col) of goal position
        - max_depth: maximum depth to explore
    
    Returns:
        - list of positions representing the path if found, else None
    """
    for depth in range(max_depth + 1):
        visited = set()
        path = []
        result = depth_limited_search(start, goal, depth, visited, path)
        if result:
            return result
    return None

# Example usage
max_depth = 20  # Reasonable max depth for the maze
result_path = iterative_deepening_dfs(start, goal, max_depth)

if result_path:
    print("Path found:", result_path)
else:
    print("No path found within the depth limit.")