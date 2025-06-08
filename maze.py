import random

def generate_maze(rows=10, cols=10):
    # Inicializa todas as células como paredes
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def in_bounds(x, y):
        return 0 <= x < rows and 0 <= y < cols

    def carve(x, y):
        maze[x][y] = 0
        dirs = [(0,1), (1,0), (0,-1), (-1,0)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx*2, y + dy*2
            if in_bounds(nx, ny) and maze[nx][ny] == 1:
                maze[x + dx][y + dy] = 0
                carve(nx, ny)

    # Começa do canto superior esquerdo
    carve(0, 0)
    # Garante que o objetivo está acessível
    maze[rows-1][cols-1] = 0
    maze[rows-1][cols-2] = 0
    maze[rows-2][cols-1] = 0
    return maze

if __name__ == '__main__':
    m = generate_maze()
    for row in m:
        print(''.join([' ' if c==0 else '#' for c in row])) 