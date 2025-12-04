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

from collections import deque

def is_valid(row, col):
    """Check if the position is within bounds and is an open path (0)."""
    return 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] == 0

def reconstruct_path(forward_came_from, backward_came_from, intersection):
    """
    Reconstruct the path from start to goal through the intersection point.
    
    Args:
        - forward_came_from: dict mapping positions to their predecessors in forward search
        - backward_came_from: dict mapping positions to their predecessors in backward search
        - intersection: meeting point of the two searches
    
    Returns:
        - list of positions representing the path
    """
    path = []
    # Reconstruct path from start to intersection
    current = intersection
    while current in forward_came_from:
        path.append(current)
        current = forward_came_from[current]
    path.append(start)
    path.reverse()
    
    # Reconstruct path from intersection to goal (excluding intersection as it's already in path)
    current = backward_came_from.get(intersection)
    while current and current in backward_came_from:
        path.append(current)
        current = backward_came_from[current]
    
    return path

def bidirectional_search(start, goal):
    """
    Perform Bidirectional Search to find a path from start to goal.
    
    Args:
        - start: tuple (row, col) of start position
        - goal: tuple (row, col) of goal position
    
    Returns:
        - list of positions representing the path if found, else None
    """
    if start == goal:
        return [start]
    
    # Initialize queues and visited sets for both directions
    forward_queue = deque([(start, [start])])
    backward_queue = deque([(goal, [goal])])
    forward_visited = {start: None}
    backward_visited = {goal: None}
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    
    while forward_queue and backward_queue:
        # Forward search
        current, forward_path = forward_queue.popleft()
        row, col = current
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            next_pos = (nr, nc)
            if is_valid(nr, nc) and next_pos not in forward_visited:
                forward_visited[next_pos] = current
                forward_queue.append((next_pos, forward_path + [next_pos]))
                # Check for intersection with backward search
                if next_pos in backward_visited:
                    return reconstruct_path(forward_visited, backward_visited, next_pos)
        
        # Backward search
        current, backward_path = backward_queue.popleft()
        row, col = current
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            next_pos = (nr, nc)
            if is_valid(nr, nc) and next_pos not in backward_visited:
                backward_visited[next_pos] = current
                backward_queue.append((next_pos, backward_path + [next_pos]))
                # Check for intersection with forward search
                if next_pos in forward_visited:
                    return reconstruct_path(forward_visited, backward_visited, next_pos)
    
    return None

# Example usage
result_path = bidirectional_search(start, goal)

if result_path:
    print("Path found:", result_path)
else:
    print("No path found.")