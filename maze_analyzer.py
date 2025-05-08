import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from pathlib import Path
import time
from maze import Maze
from maze_solver import MazeSolver
from q_learning import QLearningSolver
from cell_type import CellType

@dataclass
class AlgorithmResult:
    algorithm_name: str
    maze_size: Tuple[int, int]
    execution_time: float
    path_length: int
    cells_visited: int
    success: bool
    path: List[Tuple[int, int]]
    visited_cells: Set[Tuple[int, int]]

class MazeAnalyzer:
    def __init__(self, base_path: str = "results"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self.results: List[AlgorithmResult] = []
        
    def run_comparison(self, maze_sizes: List[int], num_mazes: int = 10,
                      algorithms: List[str] = None) -> pd.DataFrame:
        if algorithms is None:
            algorithms = ["Dijkstra", "Q-Learning"]
        all_results = []
        for size in maze_sizes:
            print(f"\nTestando labirintos {size}x{size}")
            for i in range(num_mazes):
                print(f"Labirinto {i+1}/{num_mazes}")
                maze = Maze(size, size)
                maze.generate()
                for alg_name in algorithms:
                    result = self.test_algorithm(maze, alg_name)
                    all_results.append(result)
        return self.create_results_dataframe(all_results)
    
    def test_algorithm(self, maze: Maze, algorithm_name: str) -> AlgorithmResult:
        start_time = time.time()
        if algorithm_name == "Dijkstra":
            solver = MazeSolver(maze)
            path, visited = solver.dijkstra()
            success = bool(path)
        elif algorithm_name == "Q-Learning":
            solver = QLearningSolver(maze)
            solver.train(episodes=100)
            path = solver.get_solution()
            visited = set()
            success = bool(path) and path[-1] == maze.end
        else:
            raise ValueError(f"Algoritmo {algorithm_name} não suportado")
        execution_time = time.time() - start_time
        return AlgorithmResult(
            algorithm_name=algorithm_name,
            maze_size=(maze.height, maze.width),
            execution_time=execution_time,
            path_length=len(path) if success else 0,
            cells_visited=len(visited),
            success=success,
            path=path,
            visited_cells=visited
        )
    
    def create_results_dataframe(self, results: List[AlgorithmResult]) -> pd.DataFrame:
        data = []
        for result in results:
            data.append({
                'Algorithm': result.algorithm_name,
                'Maze Size': result.maze_size[0],
                'Execution Time (s)': result.execution_time,
                'Path Length': result.path_length,
                'Cells Visited': result.cells_visited,
                'Success': result.success
            })
        return pd.DataFrame(data)
    
    def generate_analysis_report(self, df: pd.DataFrame):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.base_path / f"analysis_report_{timestamp}"
        report_path.mkdir(exist_ok=True)
        df.to_csv(report_path / "raw_data.csv", index=False)
        self.generate_visualizations(df, report_path)
        self.generate_statistical_report(df, report_path)
    
    def generate_visualizations(self, df: pd.DataFrame, report_path: Path):
        #plt.style.use('seaborn')
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df, x='Maze Size', y='Execution Time (s)', 
                    hue='Algorithm', marker='o')
        plt.title('Tempo de Execução por Tamanho do Labirinto')
        plt.savefig(report_path / 'execution_time.png')
        plt.close()
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df[df['Success']], x='Maze Size', y='Path Length', 
                    hue='Algorithm', marker='o')
        plt.title('Comprimento do Caminho por Tamanho do Labirinto')
        plt.savefig(report_path / 'path_length.png')
        plt.close()
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df, x='Maze Size', y='Cells Visited', 
                    hue='Algorithm', marker='o')
        plt.title('Células Visitadas por Tamanho do Labirinto')
        plt.savefig(report_path / 'cells_visited.png')
        plt.close()
        plt.figure(figsize=(10, 6))
        success_rates = df.groupby(['Algorithm', 'Maze Size'])['Success'].mean()
        success_rates.unstack().plot(kind='bar')
        plt.title('Taxa de Sucesso por Algoritmo e Tamanho do Labirinto')
        plt.tight_layout()
        plt.savefig(report_path / 'success_rate.png')
        plt.close()
    
    def generate_statistical_report(self, df: pd.DataFrame, report_path: Path):
        report = []
        report.append("RELATÓRIO DE ANÁLISE COMPARATIVA")
        report.append("==============================\n")
        report.append("Métricas por Algoritmo:")
        for algorithm in df['Algorithm'].unique():
            alg_data = df[df['Algorithm'] == algorithm]
            report.append(f"\n{algorithm}:")
            report.append(f"- Tempo médio de execução: {alg_data['Execution Time (s)'].mean():.4f}s")
            report.append(f"- Comprimento médio do caminho: {alg_data['Path Length'].mean():.2f}")
            report.append(f"- Média de células visitadas: {alg_data['Cells Visited'].mean():.2f}")
            report.append(f"- Taxa de sucesso: {(alg_data['Success'].mean() * 100):.1f}%")
        report.append("\nAnálise por Tamanho do Labirinto:")
        for size in sorted(df['Maze Size'].unique()):
            size_data = df[df['Maze Size'] == size]
            report.append(f"\nTamanho {size}x{size}:")
            for algorithm in df['Algorithm'].unique():
                alg_size_data = size_data[size_data['Algorithm'] == algorithm]
                report.append(f"  {algorithm}:")
                report.append(f"  - Tempo médio: {alg_size_data['Execution Time (s)'].mean():.4f}s")
                report.append(f"  - Taxa de sucesso: {(alg_size_data['Success'].mean() * 100):.1f}%")
        with open(report_path / "statistical_report.txt", "w") as f:
            f.write("\n".join(report))