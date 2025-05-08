import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from typing import Dict, Any
from pathlib import Path
import jinja2

class PerformanceAnalyzer:
    def __init__(self, results_df: pd.DataFrame):
        self.results_df = results_df
        self.metrics = {
            'execution_time': 'Execution Time (s)',
            'path_length': 'Path Length',
            'cells_visited': 'Cells Visited',
            'success_rate': 'Success Rate (%)'
        }
    
    def calculate_statistics(self) -> Dict[str, Any]:
        stats_dict = {}
        for algorithm in self.results_df['Algorithm'].unique():
            alg_data = self.results_df[self.results_df['Algorithm'] == algorithm]
            stats_dict[algorithm] = {
                'execution_time': {
                    'mean': alg_data['Execution Time (s)'].mean(),
                    'std': alg_data['Execution Time (s)'].std(),
                    'median': alg_data['Execution Time (s)'].median(),
                    'min': alg_data['Execution Time (s)'].min(),
                    'max': alg_data['Execution Time (s)'].max()
                },
                'path_length': {
                    'mean': alg_data['Path Length'].mean(),
                    'std': alg_data['Path Length'].std(),
                    'median': alg_data['Path Length'].median(),
                    'min': alg_data['Path Length'].min(),
                    'max': alg_data['Path Length'].max()
                },
                'cells_visited': {
                    'mean': alg_data['Cells Visited'].mean(),
                    'std': alg_data['Cells Visited'].std(),
                    'median': alg_data['Cells Visited'].median(),
                    'min': alg_data['Cells Visited'].min(),
                    'max': alg_data['Cells Visited'].max()
                },
                'success_rate': {
                    'percentage': (alg_data['Success'].mean() * 100)
                }
            }
        return stats_dict
    
    def perform_statistical_tests(self) -> Dict[str, Any]:
        test_results = {}
        algorithms = list(self.results_df['Algorithm'].unique())
        for metric in ['Execution Time (s)', 'Path Length', 'Cells Visited']:
            test_results[metric] = {}
            groups = [group for name, group in self.results_df.groupby('Algorithm')[metric]]
            f_stat, p_value = stats.f_oneway(*groups)
            test_results[metric]['anova'] = {
                'f_statistic': f_stat,
                'p_value': p_value
            }
            for i in range(len(algorithms)):
                for j in range(i + 1, len(algorithms)):
                    alg1, alg2 = algorithms[i], algorithms[j]
                    t_stat, p_value = stats.ttest_ind(
                        self.results_df[self.results_df['Algorithm'] == alg1][metric],
                        self.results_df[self.results_df['Algorithm'] == alg2][metric]
                    )
                    test_results[metric][f'{alg1}_vs_{alg2}'] = {
                        't_statistic': t_stat,
                        'p_value': p_value
                    }
        return test_results

class VisualizationGenerator:
    def __init__(self, results_df: pd.DataFrame, output_path: Path):
        self.results_df = results_df
        self.output_path = output_path
        self.output_path.mkdir(exist_ok=True)
        
    def generate_all_visualizations(self):
        self.performance_comparison_plot()
        self.success_rate_plot()
        self.maze_size_impact_plot()
    
    def performance_comparison_plot(self):
        plt.figure(figsize=(15, 10))
        plt.subplot(2, 2, 1)
        sns.boxplot(data=self.results_df, x='Algorithm', y='Execution Time (s)')
        plt.title('Tempo de Execução por Algoritmo')
        plt.xticks(rotation=45)
        plt.subplot(2, 2, 2)
        sns.boxplot(data=self.results_df, x='Algorithm', y='Path Length')
        plt.title('Comprimento do Caminho por Algoritmo')
        plt.xticks(rotation=45)
        plt.subplot(2, 2, 3)
        sns.boxplot(data=self.results_df, x='Algorithm', y='Cells Visited')
        plt.title('Células Visitadas por Algoritmo')
        plt.xticks(rotation=45)
        plt.subplot(2, 2, 4)
        success_rates = self.results_df.groupby('Algorithm')['Success'].mean() * 100
        success_rates.plot(kind='bar')
        plt.title('Taxa de Sucesso por Algoritmo')
        plt.ylabel('Taxa de Sucesso (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(self.output_path / 'performance_comparison.png')
        plt.close()
    
    def success_rate_plot(self):
        plt.figure(figsize=(10, 6))
        success_rates = self.results_df.groupby(['Algorithm', 'Maze Size'])['Success'].mean()
        success_rates.unstack().plot(kind='bar')
        plt.title('Taxa de Sucesso por Algoritmo e Tamanho do Labirinto')
        plt.ylabel('Taxa de Sucesso')
        plt.tight_layout()
        plt.savefig(self.output_path / 'success_rate.png')
        plt.close()
    
    def maze_size_impact_plot(self):
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=self.results_df, x='Maze Size', y='Execution Time (s)', 
                    hue='Algorithm', marker='o')
        plt.title('Tempo de Execução por Tamanho do Labirinto')
        plt.savefig(self.output_path / 'maze_size_impact_time.png')
        plt.close()
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=self.results_df[self.results_df['Success']], 
                    x='Maze Size', y='Path Length', 
                    hue='Algorithm', marker='o')
        plt.title('Comprimento do Caminho por Tamanho do Labirinto')
        plt.savefig(self.output_path / 'maze_size_impact_path.png')
        plt.close()

class ReportGenerator:
    def __init__(self, results_df: pd.DataFrame, stats_dict: Dict[str, Any],
                 test_results: Dict[str, Any], output_path: Path):
        self.results_df = results_df
        self.stats_dict = stats_dict
        self.test_results = test_results
        self.output_path = output_path
    
    def generate_full_report(self):
        report_template = """
# Relatório de Análise Comparativa de Algoritmos de Pathfinding

## Sumário Executivo

Este relatório apresenta uma análise comparativa detalhada dos algoritmos de pathfinding
implementados para resolução de labirintos.

## Métricas de Performance

{% for algorithm, metrics in stats_dict.items() %}
### {{ algorithm }}

- **Tempo de Execução**:
  - Média: {{ "%.4f"|format(metrics.execution_time.mean) }}s
  - Desvio Padrão: {{ "%.4f"|format(metrics.execution_time.std) }}s
  - Mediana: {{ "%.4f"|format(metrics.execution_time.median) }}s
  - Min/Max: {{ "%.4f"|format(metrics.execution_time.min) }}s / {{ "%.4f"|format(metrics.execution_time.max) }}s

- **Comprimento do Caminho**:
  - Média: {{ "%.2f"|format(metrics.path_length.mean) }}
  - Desvio Padrão: {{ "%.2f"|format(metrics.path_length.std) }}
  - Min/Max: {{ metrics.path_length.min }}/{{ metrics.path_length.max }}

- **Células Visitadas**:
  - Média: {{ "%.2f"|format(metrics.cells_visited.mean) }}
  - Desvio Padrão: {{ "%.2f"|format(metrics.cells_visited.std) }}
  - Min/Max: {{ metrics.cells_visited.min }}/{{ metrics.cells_visited.max }}

- **Taxa de Sucesso**: {{ "%.1f"|format(metrics.success_rate.percentage) }}%

{% endfor %}

## Análise Estatística

{% for metric, tests in test_results.items() %}
### {{ metric }}

#### ANOVA
- F-statistic: {{ "%.4f"|format(tests.anova.f_statistic) }}
- p-value: {{ "%.4f"|format(tests.anova.p_value) }}

#### Comparações Pareadas
{% for test_name, test_data in tests.items() %}
{% if test_name != 'anova' %}
- **{{ test_name }}**:
  - t-statistic: {{ "%.4f"|format(test_data.t_statistic) }}
  - p-value: {{ "%.4f"|format(test_data.p_value) }}
{% endif %}
{% endfor %}

{% endfor %}

## Conclusões

Com base nas análises realizadas, podemos concluir que:

1. **Tempo de Execução**: {% if stats_dict|length > 0 %}
   O algoritmo mais rápido foi {{ fastest_algorithm }} com tempo médio de {{ fastest_time }}s.
   {% endif %}

2. **Qualidade da Solução**: {% if stats_dict|length > 0 %}
   O algoritmo com menor comprimento médio de caminho foi {{ best_path_algorithm }}.
   {% endif %}

3. **Eficiência de Exploração**: {% if stats_dict|length > 0 %}
   O algoritmo que visitou menos células foi {{ most_efficient_algorithm }}.
   {% endif %}

## Recomendações

Com base nos resultados obtidos, recomendamos:

1. Para labirintos pequenos: {{ small_maze_recommendation }}
2. Para labirintos grandes: {{ large_maze_recommendation }}
3. Para melhor compromisso tempo/qualidade: {{ balanced_recommendation }}

"""
        template_data = self._prepare_template_data()
        template = jinja2.Template(report_template)
        report_content = template.render(**template_data)
        with open(self.output_path / 'report.txt', 'w') as f:
            f.write(report_content)
    
    def _prepare_template_data(self) -> Dict[str, Any]:
        template_data = {
            'stats_dict': self.stats_dict,
            'test_results': self.test_results
        }
        mean_times = {alg: stats['execution_time']['mean'] 
                     for alg, stats in self.stats_dict.items()}
        fastest_algorithm = min(mean_times, key=mean_times.get)
        template_data['fastest_algorithm'] = fastest_algorithm
        template_data['fastest_time'] = f"{mean_times[fastest_algorithm]:.4f}"
        mean_paths = {alg: stats['path_length']['mean'] 
                     for alg, stats in self.stats_dict.items()}
        best_path_algorithm = min(mean_paths, key=mean_paths.get)
        template_data['best_path_algorithm'] = best_path_algorithm
        mean_visits = {alg: stats['cells_visited']['mean'] 
                      for alg, stats in self.stats_dict.items()}
        most_efficient_algorithm = min(mean_visits, key=mean_visits.get)
        template_data['most_efficient_algorithm'] = most_efficient_algorithm
        template_data.update(self._generate_recommendations())
        return template_data
    
    def _generate_recommendations(self) -> Dict[str, str]:
        small_maze_data = self.results_df[self.results_df['Maze Size'] <= 20]
        large_maze_data = self.results_df[self.results_df['Maze Size'] > 20]
        small_maze_perf = small_maze_data.groupby('Algorithm').agg({
            'Execution Time (s)': 'mean',
            'Path Length': 'mean',
            'Success': 'mean'
        })
        small_maze_best = small_maze_perf.index[0]
        large_maze_perf = large_maze_data.groupby('Algorithm').agg({
            'Execution Time (s)': 'mean',
            'Path Length': 'mean',
            'Success': 'mean'
        })
        large_maze_best = large_maze_perf.index[0]
        balanced_score = self.results_df.groupby('Algorithm').agg({
            'Execution Time (s)': lambda x: 1/x.mean(),
            'Path Length': lambda x: 1/x.mean(),
            'Success': 'mean'
        }).mean(axis=1)
        balanced_best = balanced_score.index[balanced_score.argmax()]
        return {
            'small_maze_recommendation': small_maze_best,
            'large_maze_recommendation': large_maze_best,
            'balanced_recommendation': balanced_best
        }

def generate_comprehensive_report(results_df: pd.DataFrame, output_path: Path) -> Dict[str, Any]:
    output_path.mkdir(exist_ok=True)
    analyzer = PerformanceAnalyzer(results_df)
    stats_dict = analyzer.calculate_statistics()
    test_results = analyzer.perform_statistical_tests()
    viz_generator = VisualizationGenerator(results_df, output_path / 'visualizations')
    viz_generator.generate_all_visualizations()
    report_generator = ReportGenerator(results_df, stats_dict, test_results, output_path)
    report_generator.generate_full_report()
    return {
        'statistics': stats_dict,
        'test_results': test_results,
        'report_path': output_path / 'report.txt',
        'visualizations_path': output_path / 'visualizations'
    }