from queue import PriorityQueue
from typing import List, Tuple, Set
from maze import Maze
from cell_type import CellType

class MazeSolver:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.visited = set()
        self.path = []
        
    def dijkstra(self) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
        start = self.maze.start
        end = self.maze.end
        distances = {(i, j): float('inf') 
                    for i in range(self.maze.height) 
                    for j in range(self.maze.width)}
        distances[start] = 0
        pq = PriorityQueue()
        pq.put((0, start))
        previous = {}
        visited = set()
        
        while not pq.empty():
            current_dist, current = pq.get()
            if current == end:
                break
            if current in visited:
                continue
            visited.add(current)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_x = current[1] + dx
                next_y = current[0] + dy
                if (0 <= next_x < self.maze.width and 
                    0 <= next_y < self.maze.height and 
                    self.maze.grid[next_y][next_x] != CellType.WALL.value):
                    distance = current_dist + 1
                    if distance < distances[(next_y, next_x)]:
                        distances[(next_y, next_x)] = distance
                        previous[(next_y, next_x)] = current
                        pq.put((distance, (next_y, next_x)))
        
        path = []
        current = end
        while current in previous:
            path.append(current)
            current = previous[current]
        path.append(start)
        path.reverse()
        return path, visited