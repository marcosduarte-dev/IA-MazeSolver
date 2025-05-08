import numpy as np
import random
from collections import defaultdict
from typing import List, Tuple, Dict
from maze import Maze
from cell_type import CellType
from maze_visualizer import MazeVisualizer

class QLearningAgent:
    def __init__(self, maze: Maze, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.maze = maze
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
    def get_state_key(self, state: Tuple[int, int]) -> str:
        return f"{state[0]},{state[1]}"
    
    def get_valid_actions(self, state: Tuple[int, int]) -> List[Tuple[int, int]]:
        valid_actions = []
        for action in self.actions:
            new_y = state[0] + action[0]
            new_x = state[1] + action[1]
            if (0 <= new_x < self.maze.width and 
                0 <= new_y < self.maze.height and 
                self.maze.grid[new_y][new_x] != CellType.WALL.value):
                valid_actions.append(action)
        return valid_actions
    
    def choose_action(self, state: Tuple[int, int]) -> Tuple[int, int]:
        if random.random() < self.epsilon:
            return random.choice(self.get_valid_actions(state))
        state_key = self.get_state_key(state)
        valid_actions = self.get_valid_actions(state)
        if not valid_actions:
            return None
        return max(valid_actions, 
                  key=lambda a: self.q_table[state_key][str(a)])
    
    def update(self, state: Tuple[int, int], action: Tuple[int, int], 
               reward: float, next_state: Tuple[int, int]):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        action_key = str(action)
        next_max_q = max([self.q_table[next_state_key][str(a)] 
                         for a in self.get_valid_actions(next_state)], 
                        default=0)
        current_q = self.q_table[state_key][action_key]
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * next_max_q - current_q)
        self.q_table[state_key][action_key] = new_q

class MazeEnvironment:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.current_state = self.maze.start
        self.steps = 0
        self.max_steps = maze.width * maze.height * 2
        
    def reset(self) -> Tuple[int, int]:
        self.current_state = self.maze.start
        self.steps = 0
        return self.current_state
    
    def step(self, action: Tuple[int, int]) -> Tuple[Tuple[int, int], float, bool]:
        self.steps += 1
        new_y = self.current_state[0] + action[0]
        new_x = self.current_state[1] + action[1]
        new_state = (new_y, new_x)
        if (new_x < 0 or new_x >= self.maze.width or 
            new_y < 0 or new_y >= self.maze.height or 
            self.maze.grid[new_y][new_x] == CellType.WALL.value):
            return self.current_state, -1, False
        self.current_state = new_state
        if self.current_state == self.maze.end:
            return new_state, 100, True
        if self.steps >= self.max_steps:
            return new_state, -1, True
        return new_state, -0.1, False

class QLearningSolver:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.env = MazeEnvironment(maze)
        self.agent = QLearningAgent(maze)
        self.training_stats = []
    
    def train(self, episodes: int, visualizer: MazeVisualizer = None) -> List[Dict]:
        for episode in range(episodes):
            state = self.env.reset()
            total_reward = 0
            steps = 0
            while True:
                action = self.agent.choose_action(state)
                if action is None:
                    break
                next_state, reward, done = self.env.step(action)
                self.agent.update(state, action, reward, next_state)
                total_reward += reward
                steps += 1
                if visualizer and episode % 100 == 0:
                    visualizer.draw(visited=set(), 
                                  path=self.get_current_path())
                if done:
                    break
                state = next_state
            self.training_stats.append({
                'episode': episode,
                'total_reward': total_reward,
                'steps': steps
            })
            self.agent.epsilon = max(0.01, self.agent.epsilon * 0.995)
            if episode % 100 == 0:
                print(f"Episódio {episode}: Recompensa = {total_reward:.2f}, "
                      f"Passos = {steps}")
        return self.training_stats
    
    def get_solution(self) -> List[Tuple[int, int]]:
        path = [self.maze.start]
        current_state = self.maze.start
        while current_state != self.maze.end:
            state_key = self.agent.get_state_key(current_state)
            valid_actions = self.agent.get_valid_actions(current_state)
            if not valid_actions:
                break
            best_action = max(valid_actions, 
                            key=lambda a: self.agent.q_table[state_key][str(a)])
            new_y = current_state[0] + best_action[0]
            new_x = current_state[1] + best_action[1]
            current_state = (new_y, new_x)
            path.append(current_state)
            if len(path) > self.maze.width * self.maze.height:
                break
        return path
    
    def get_current_path(self) -> List[Tuple[int, int]]:
        return self.get_solution()
    
    def plot_training_stats(self):
        import matplotlib.pyplot as plt
        episodes = [stat['episode'] for stat in self.training_stats]
        rewards = [stat['total_reward'] for stat in self.training_stats]
        steps = [stat['steps'] for stat in self.training_stats]
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(episodes, rewards)
        plt.title('Recompensas por Episódio')
        plt.xlabel('Episódio')
        plt.ylabel('Recompensa Total')
        plt.subplot(1, 2, 2)
        plt.plot(episodes, steps)
        plt.title('Passos por Episódio')
        plt.xlabel('Episódio')
        plt.ylabel('Número de Passos')
        plt.tight_layout()
        plt.savefig('training_stats.png')