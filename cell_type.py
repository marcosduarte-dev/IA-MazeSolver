from enum import Enum

class CellType(Enum):
    WALL = 0
    PATH = 1
    START = 2
    END = 3
    VISITED = 4
    SOLUTION = 5