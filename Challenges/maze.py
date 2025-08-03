from collections import deque

def min_steps_with_teleports(maze):
    n = len(maze)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    teleports = [(i, j) for i in range(n) for j in range(n) if maze[i][j] == 2]
    visited = [[False] * n for _ in range(n)]
    queue = deque([(0, 0, 0)])  # (x, y, steps)
    visited[0][0] = True

    while queue:
        x, y, steps = queue.popleft()


        if (x, y) == (n - 1, n - 1):
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and maze[nx][ny] != 1:
                visited[nx][ny] = True
                queue.append((nx, ny, steps + 1))

        if maze[x][y] == 2:
            for tx, ty in teleports:
                if not visited[tx][ty]:
                    visited[tx][ty] = True
                    queue.append((tx, ty, steps + 1))

    return -1

maze = [
    [0, 1, 2],
    [0, 1, 0],
    [2, 0, 0]
]

print(min_steps_with_teleports(maze))
