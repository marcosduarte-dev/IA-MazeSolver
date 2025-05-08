import pygame
from typing import List
from maze import Maze
from maze_analyzer import AlgorithmResult
from cell_type import CellType

class BenchmarkVisualizer:
    def __init__(self, screen_width: int = 1200, screen_height: int = 800):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Benchmark Visualization")
        self.font = pygame.font.Font(None, 36)
        
    def visualize_comparison(self, maze: Maze, results: List[AlgorithmResult]):
        cell_size = min(self.screen.get_width() // (len(results) * maze.width),
                       self.screen.get_height() // maze.height)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((255, 255, 255))
            for i, result in enumerate(results):
                x_offset = i * (maze.width * cell_size + 50)
                self.draw_maze(maze, cell_size, x_offset, 0)
                if result.success:
                    self.draw_solution(result, cell_size, x_offset, 0)
                self.draw_info(result, x_offset, maze.height * cell_size + 10)
            pygame.display.flip()
        pygame.quit()
    
    def draw_maze(self, maze: Maze, cell_size: int, x_offset: int, y_offset: int):
        for y in range(maze.height):
            for x in range(maze.width):
                rect = pygame.Rect(
                    x_offset + x * cell_size,
                    y_offset + y * cell_size,
                    cell_size,
                    cell_size
                )
                color = (0, 0, 0) if maze.grid[y][x] == CellType.WALL.value else (255, 255, 255)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (128, 128, 128), rect, 1)
    
    def draw_solution(self, result: AlgorithmResult, cell_size: int, 
                     x_offset: int, y_offset: int):
        for cell in result.visited_cells:
            rect = pygame.Rect(
                x_offset + cell[1] * cell_size,
                y_offset + cell[0] * cell_size,
                cell_size,
                cell_size
            )
            pygame.draw.rect(self.screen, (200, 200, 255), rect)
        for i in range(len(result.path) - 1):
            start = result.path[i]
            end = result.path[i + 1]
            start_pos = (
                x_offset + start[1] * cell_size + cell_size // 2,
                y_offset + start[0] * cell_size + cell_size // 2
            )
            end_pos = (
                x_offset + end[1] * cell_size + cell_size // 2,
                y_offset + end[0] * cell_size + cell_size // 2
            )
            pygame.draw.line(self.screen, (255, 0, 0), start_pos, end_pos, 2)
    
    def draw_info(self, result: AlgorithmResult, x_offset: int, y_pos: int):
        info_text = [
            f"Algorithm: {result.algorithm_name}",
            f"Time: {result.execution_time:.3f}s",
            f"Path Length: {result.path_length}",
            f"Cells Visited: {result.cells_visited}"
        ]
        for i, text in enumerate(info_text):
            surface = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(surface, (x_offset, y_pos + i * 30))