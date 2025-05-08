import pygame
from typing import List, Tuple, Set
from maze import Maze
from cell_type import CellType

class MazeVisualizer:
    def __init__(self, maze: Maze, cell_size: int = 20):
        self.maze = maze
        self.cell_size = cell_size
        self.width = maze.width * cell_size
        self.height = maze.height * cell_size
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Solver")
        self.colors = {
            CellType.WALL: (0, 0, 0),
            CellType.PATH: (255, 255, 255),
            CellType.START: (0, 255, 0),
            CellType.END: (255, 0, 0),
            CellType.VISITED: (150, 150, 255),
            CellType.SOLUTION: (255, 255, 0)
        }
        
    def draw(self, visited: Set[Tuple[int, int]] = None, 
            path: List[Tuple[int, int]] = None):
        self.screen.fill((255, 255, 255))
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell_type = CellType(self.maze.grid[y][x])
                color = self.colors[cell_type]
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, color, rect)
        if visited:
            for cell in visited:
                if cell != self.maze.start and cell != self.maze.end:
                    rect = pygame.Rect(
                        cell[1] * self.cell_size,
                        cell[0] * self.cell_size,
                        self.cell_size,
                        self.cell_size
                    )
                    pygame.draw.rect(self.screen, self.colors[CellType.VISITED], rect)
        if path:
            for cell in path:
                if cell != self.maze.start and cell != self.maze.end:
                    rect = pygame.Rect(
                        cell[1] * self.cell_size,
                        cell[0] * self.cell_size,
                        self.cell_size,
                        self.cell_size
                    )
                    pygame.draw.rect(self.screen, self.colors[CellType.SOLUTION], rect)
        pygame.display.flip()