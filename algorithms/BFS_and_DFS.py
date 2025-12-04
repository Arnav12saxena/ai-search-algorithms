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

# Helper function to check if move is valid
def is_valid_move(maze, visited, x, y):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and not visited[x][y] and maze[x][y] == 0

# BFS implementation using List as a queue
def bfs(maze, start, goal):
    queue = [(start, [start])]
    visited = [[False]*len(maze[0]) for _ in range(len(maze))]
    visited[start[0]][start[1]] = True
    
    while queue:
        (x, y), path = queue.pop(0)  # FIFO behavior using List
        if (x, y) == goal:
            return path
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x+dx, y+dy
            if is_valid_move(maze, visited, nx, ny):
                visited[nx][ny] = True
                queue.append(((nx, ny), path + [(nx, ny)]))
    return None

# DFS implementation using stack
def dfs(maze, start, goal):
    stack = [(start, [start])]
    visited = [[False]*len(maze[0]) for _ in range(len(maze))]
    visited[start[0]][start[1]] = True
    
    while stack:
        (x, y), path = stack.pop()
        if (x, y) == goal:
            return path
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x+dx, y+dy
            if is_valid_move(maze, visited, nx, ny):
                visited[nx][ny] = True
                stack.append(((nx, ny), path + [(nx, ny)]))
    return None

# Run BFS and DFS
bfs_path = bfs(maze, start, goal)
dfs_path = dfs(maze, start, goal)

print("BFS Path:", bfs_path)
print("DFS Path:", dfs_path)