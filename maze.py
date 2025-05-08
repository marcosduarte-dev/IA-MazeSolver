import numpy as np
import random
from cell_type import CellType

class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        self.start = None
        self.end = None
        
    def generate(self):
        self.grid.fill(CellType.WALL.value)
        start_x, start_y = 1, 1
        self.recursive_backtrack(start_x, start_y)
        self.set_start_end()
        
    def recursive_backtrack(self, x: int, y: int):
        self.grid[y][x] = CellType.PATH.value
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.width and 
                0 <= new_y < self.height and 
                self.grid[new_y][new_x] == CellType.WALL.value):
                self.grid[y + dy//2][x + dx//2] = CellType.PATH.value
                self.recursive_backtrack(new_x, new_y)
    
    def set_start_end(self):
        paths = [(i, j) for i in range(self.height) 
                for j in range(self.width) 
                if self.grid[i][j] == CellType.PATH.value]
        self.start = random.choice(paths)
        paths.remove(self.start)
        max_dist = 0
        for path in paths:
            dist = abs(path[0] - self.start[0]) + abs(path[1] - self.start[1])
            if dist > max_dist:
                max_dist = dist
                self.end = path
        self.grid[self.start[0]][self.start[1]] = CellType.START.value
        self.grid[self.end[0]][self.end[1]] = CellType.END.value