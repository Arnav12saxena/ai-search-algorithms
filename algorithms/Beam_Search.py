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

def beam_search(start, goal, beam_width=2):
    """
    Perform Beam Search to find a path from start to goal.
    
    Args:
        - start: tuple (row, col) of start position
        - goal: tuple (row, col) of goal position
        - beam_width: number of paths to keep at each step
    
    Returns:
        - list of positions representing the path if found, else None
    """
    # Priority queue to store (heuristic, current_position, path)
    queue = [(manhattan_distance(start, goal), start, [start])]
    visited = set()
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    
    while queue:
        # Select top beam_width paths
        current_level = []
        while queue and len(current_level) < beam_width:
            h_score, current, path = heappop(queue)
            if current not in visited:
                current_level.append((h_score, current, path))
        
        # If goal is found in current level, return the path
        for _, current, path in current_level:
            if current == goal:
                return path
        
        # Mark current level nodes as visited
        for _, current, _ in current_level:
            visited.add(current)
        
        # Generate successors for current level
        next_queue = []
        for _, current, path in current_level:
            row, col = current
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                next_pos = (nr, nc)
                if is_valid(nr, nc) and next_pos not in visited:
                    new_path = path + [next_pos]
                    heappush(next_queue, (manhattan_distance(next_pos, goal), next_pos, new_path))
        
        # Keep only the top beam_width paths for the next iteration
        queue = []
        for _ in range(min(beam_width, len(next_queue))):
            if next_queue:
                heappush(queue, heappop(next_queue))
    
    return None

# Example usage
beam_width = 2  # Adjust beam width as needed
result_path = beam_search(start, goal, beam_width)

if result_path:
    print("Path found:", result_path)
else:
    print("No path found.")