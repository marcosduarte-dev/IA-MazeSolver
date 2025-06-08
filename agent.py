import numpy as np
import pickle
import os

class QLearningAgent:
    def __init__(self, rows=10, cols=10, actions=4, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.rows = rows
        self.cols = cols
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros((rows, cols, actions))

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.actions)
        return np.argmax(self.q_table[state[0], state[1]])

    def train(self, maze, start, goal, episodes=2000, max_steps=500):
        for ep in range(episodes):
            state = start
            for _ in range(max_steps):
                action = self.choose_action(state)
                next_state, reward, done = self.step(maze, state, action, goal)
                old_value = self.q_table[state[0], state[1], action]
                next_max = np.max(self.q_table[next_state[0], next_state[1]])
                self.q_table[state[0], state[1], action] = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
                state = next_state
                if done:
                    break

    def step(self, maze, state, action, goal):
        moves = [(-1,0), (0,1), (1,0), (0,-1)]
        x, y = state
        dx, dy = moves[action]
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.rows and 0 <= ny < self.cols and maze[nx][ny] == 0:
            next_state = (nx, ny)
        else:
            next_state = state  # bateu na parede
        if next_state == goal:
            return next_state, 10, True
        else:
            return next_state, -1, False

    def get_policy_path_with_steps(self, maze, start, goal, max_steps=500):
        state = start
        path = [state]
        total_steps = 1
        visited = set([start])  # Conjunto para rastrear estados visitados
        
        for _ in range(max_steps):
            action = np.argmax(self.q_table[state[0], state[1]])
            moves = [(-1,0), (0,1), (1,0), (0,-1)]
            x, y = state
            dx, dy = moves[action]
            nx, ny = x + dx, y + dy
            
            # Incrementa o contador de passos mesmo se bater na parede
            total_steps += 1
            
            if 0 <= nx < self.rows and 0 <= ny < self.cols and maze[nx][ny] == 0:
                next_state = (nx, ny)
                if next_state not in visited:  # Só adiciona ao caminho se for um novo estado
                    path.append(next_state)
                    visited.add(next_state)
            else:
                next_state = state
                
            if next_state == state:
                break  # preso
                
            state = next_state
            if state == goal:
                break
                
        return path, total_steps

    def save_qtable(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_qtable(self, filename):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
        else:
            raise FileNotFoundError(f"Arquivo {filename} não encontrado.") 