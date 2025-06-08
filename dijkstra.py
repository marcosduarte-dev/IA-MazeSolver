import heapq

def dijkstra(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    dist = [[float('inf') for _ in range(cols)] for _ in range(rows)]
    prev = [[None for _ in range(cols)] for _ in range(rows)]
    dist[start[0]][start[1]] = 0
    heap = [(0, start)]
    moves = [(-1,0), (0,1), (1,0), (0,-1)]
    total_steps = 0

    while heap:
        d, (x, y) = heapq.heappop(heap)
        total_steps += 1  # Conta cada nó visitado
        
        if visited[x][y]:
            continue
        visited[x][y] = True
        if (x, y) == goal:
            break
            
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                if dist[nx][ny] > d + 1:
                    dist[nx][ny] = d + 1
                    prev[nx][ny] = (x, y)
                    heapq.heappush(heap, (dist[nx][ny], (nx, ny)))
                    total_steps += 1  # Conta cada aresta explorada

    # Reconstruir caminho
    path = []
    curr = goal
    while curr and dist[curr[0]][curr[1]] != float('inf'):
        path.append(curr)
        curr = prev[curr[0]][curr[1]]
    path.reverse()
    if path and path[0] == start:
        return path, total_steps
    else:
        return [], total_steps

if __name__ == '__main__':
    # Exemplo de uso
    maze = [[0,1,0,0],[0,1,0,1],[0,0,0,1],[1,1,0,0]]
    path, steps = dijkstra(maze, (0,0), (3,3))
    print(f"Caminho: {path}")
    print(f"Total de passos: {steps}") 