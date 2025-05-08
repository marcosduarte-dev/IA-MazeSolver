import pygame
from maze import Maze
from maze_visualizer import MazeVisualizer
from maze_solver import MazeSolver
from q_learning import QLearningSolver
from maze_analyzer import MazeAnalyzer
from benchmark_visualizer import BenchmarkVisualizer
from performance_analyzer import generate_comprehensive_report
from pathlib import Path

def test_dijkstra():
    maze = Maze(20, 20)
    maze.generate()
    visualizer = MazeVisualizer(maze, cell_size=30)
    solver = MazeSolver(maze)
    path, visited = solver.dijkstra()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        visualizer.draw(visited, path)
        pygame.time.delay(50)
    pygame.quit()

def test_q_learning():
    maze = Maze(10, 10)
    maze.generate()
    visualizer = MazeVisualizer(maze, cell_size=30)
    solver = QLearningSolver(maze)
    stats = solver.train(1000, visualizer)
    solution = solver.get_solution()
    solver.plot_training_stats()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        visualizer.draw(visited=set(), path=solution)
        pygame.time.delay(50)
    pygame.quit()

def run_benchmark():
    maze_sizes = [10, 20, 30]
    num_mazes = 5
    algorithms = ["Dijkstra", "Q-Learning"]
    analyzer = MazeAnalyzer()
    results_df = analyzer.run_comparison(maze_sizes, num_mazes, algorithms)
    analyzer.generate_analysis_report(results_df)
    maze = Maze(20, 20)
    maze.generate()
    results = [analyzer.test_algorithm(maze, alg) for alg in algorithms]
    visualizer = BenchmarkVisualizer()
    visualizer.visualize_comparison(maze, results)
    output_dir = Path('analysis_results')
    report_info = generate_comprehensive_report(results_df, output_dir)
    print(f"Relatório gerado em: {report_info['report_path']}")
    print(f"Visualizações disponíveis em: {report_info['visualizations_path']}")

if __name__ == "__main__":
    run_benchmark()
    # Para testes individuais, descomente:
    # test_dijkstra()
    # test_q_learning()