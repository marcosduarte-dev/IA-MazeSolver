# Maze Solver - RL vs Dijkstra

Este projeto implementa um solucionador de labirintos que compara dois algoritmos diferentes: Aprendizado por Reforço (Q-Learning) e Dijkstra. O projeto inclui uma interface gráfica interativa que permite visualizar e comparar o desempenho dos dois algoritmos.

## Características

- Geração aleatória de labirintos
- Implementação de Q-Learning para resolução
- Implementação do algoritmo de Dijkstra
- Interface gráfica interativa
- Visualização em tempo real do processo de resolução
- Comparação de desempenho entre os algoritmos
- Geração de lotes de testes
- Exportação de resultados para CSV
- Salvamento e carregamento de tabelas Q

## Requisitos

- Python 3.x
- NumPy
- Tkinter (geralmente incluído com Python)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/maze-solver.git
cd maze-solver
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

Execute o programa principal:
```bash
python main.py
```

### Interface Gráfica

A interface gráfica oferece várias funcionalidades:

- **Gerar Labirinto**: Cria um novo labirinto aleatório
- **Treinar Agente**: Treina o agente de Q-Learning
- **Resolver RL**: Resolve o labirinto usando Q-Learning
- **Resolver Dijkstra**: Resolve o labirinto usando o algoritmo de Dijkstra
- **Zoom**: Controles para ajustar a visualização
- **Gerar Lote**: Gera múltiplos labirintos para testes

### Geração de Lotes

Para gerar lotes de testes:
1. Defina o tamanho mínimo e máximo do labirinto
2. Especifique a quantidade de labirintos
3. Clique em "Gerar Lote"

Os resultados serão salvos automaticamente em `results.csv`.

## Estrutura do Projeto

- `main.py`: Ponto de entrada do programa
- `ui.py`: Implementação da interface gráfica
- `maze.py`: Geração de labirintos
- `agent.py`: Implementação do agente de Q-Learning
- `dijkstra.py`: Implementação do algoritmo de Dijkstra
- `utils.py`: Funções utilitárias
- `requirements.txt`: Dependências do projeto

## Análise de Desempenho

O programa registra as seguintes métricas para cada algoritmo:
- Tamanho do caminho encontrado
- Tempo de execução
- Número total de passos
- Taxa de sucesso

Os resultados são salvos em `results.csv` para análise posterior.