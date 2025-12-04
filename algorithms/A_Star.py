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

def manhattan_distance(pos1, pos2):
    """Calculate Manhattan distance between two positions."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def a_star_search(start, goal):
    """
    Perform A* Search to find the shortest path from start to goal.
    
    Args:
        - start: tuple (row, col) of start position
        - goal: tuple (row, col) of goal position
    
    Returns:
        - list of positions representing the shortest path if found, else None
    """
    # Priority queue to store (f_score, current_position, path)
    queue = [(0 + manhattan_distance(start, goal), start, [start])]
    visited = set()
    g_scores = {start: 0}  # Track actual cost from start to each node
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    
    while queue:
        f_score, current, path = heappop(queue)
        row, col = current
        
        if current == goal:
            return path
        
        if current in visited:
            continue
        
        visited.add(current)
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            next_pos = (nr, nc)
            if is_valid(nr, nc) and next_pos not in visited:
                new_g_score = g_scores[current] + 1  # Cost of each move is 1
                if next_pos not in g_scores or new_g_score < g_scores[next_pos]:
                    g_scores[next_pos] = new_g_score
                    f_score = new_g_score + manhattan_distance(next_pos, goal)
                    new_path = path + [next_pos]
                    heappush(queue, (f_score, next_pos, new_path))
    
    return None

# Example usage
result_path = a_star_search(start, goal)

if result_path:
    print("Path found:", result_path)
else:
    print("No path found.")