import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from maze import generate_maze
from agent import QLearningAgent
from dijkstra import dijkstra
from utils import export_to_csv
import time
import random

class MazeUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Maze Solver - RL vs Dijkstra')
        self.geometry('800x600')  # Aumentado para melhor visualização
        self.resizable(False, False)
        self.cell_size = 40
        self.zoom_level = 1.0
        self.rows = 10
        self.cols = 10
        self.maze = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.agent_pos = (0, 0)
        self.goal_pos = (9, 9)
        self.agent = QLearningAgent(self.rows, self.cols)
        self.maze_id = 1
        self.create_widgets()
        self.draw_maze()

    def create_widgets(self):
        # Frame para inputs de tamanho
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)
        
        # Labels e inputs para tamanho mínimo
        tk.Label(input_frame, text="Tamanho Mínimo:").grid(row=0, column=0, padx=5)
        self.min_size = tk.Entry(input_frame, width=10)
        self.min_size.insert(0, "10")
        self.min_size.grid(row=0, column=1, padx=5)
        
        # Labels e inputs para tamanho máximo
        tk.Label(input_frame, text="Tamanho Máximo:").grid(row=0, column=2, padx=5)
        self.max_size = tk.Entry(input_frame, width=10)
        self.max_size.insert(0, "100")
        self.max_size.grid(row=0, column=3, padx=5)
        
        # Labels e inputs para quantidade
        tk.Label(input_frame, text="Quantidade:").grid(row=0, column=4, padx=5)
        self.quantity = tk.Entry(input_frame, width=10)
        self.quantity.insert(0, "5")
        self.quantity.grid(row=0, column=5, padx=5)
        
        # Botão para gerar lotes
        self.btn_batch = tk.Button(input_frame, text='Gerar Lote', command=self.generate_batch)
        self.btn_batch.grid(row=0, column=6, padx=5)

        # Frame para controles de zoom
        zoom_frame = tk.Frame(self)
        zoom_frame.pack(pady=5)
        
        tk.Label(zoom_frame, text="Zoom:").pack(side=tk.LEFT, padx=5)
        self.btn_zoom_in = tk.Button(zoom_frame, text="+", command=self.zoom_in)
        self.btn_zoom_in.pack(side=tk.LEFT, padx=2)
        self.btn_zoom_out = tk.Button(zoom_frame, text="-", command=self.zoom_out)
        self.btn_zoom_out.pack(side=tk.LEFT, padx=2)
        self.btn_zoom_reset = tk.Button(zoom_frame, text="Reset", command=self.zoom_reset)
        self.btn_zoom_reset.pack(side=tk.LEFT, padx=2)

        # Frame para o canvas com scrollbars
        canvas_frame = tk.Frame(self)
        canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        self.h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.v_scrollbar = tk.Scrollbar(canvas_frame)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas com scrollbars
        self.canvas = tk.Canvas(canvas_frame, 
                              width=600, 
                              height=600,
                              bg='white',
                              xscrollcommand=self.h_scrollbar.set,
                              yscrollcommand=self.v_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)
        
        # Frame para botões
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        self.btn_generate = tk.Button(btn_frame, text='Gerar Labirinto', command=self.generate_maze)
        self.btn_generate.grid(row=0, column=0, padx=5)
        
        self.btn_train = tk.Button(btn_frame, text='Treinar Agente', command=self.train_agent)
        self.btn_train.grid(row=0, column=1, padx=5)
        
        self.btn_solve_rl = tk.Button(btn_frame, text='Resolver RL', command=self.solve_rl)
        self.btn_solve_rl.grid(row=0, column=2, padx=5)
        
        self.btn_solve_dijkstra = tk.Button(btn_frame, text='Resolver Dijkstra', command=self.solve_dijkstra)
        self.btn_solve_dijkstra.grid(row=0, column=3, padx=5)

    def zoom_in(self):
        self.zoom_level *= 1.2
        self.update_canvas_size()
        self.draw_maze()

    def zoom_out(self):
        self.zoom_level /= 1.2
        self.update_canvas_size()
        self.draw_maze()

    def zoom_reset(self):
        self.zoom_level = 1.0
        self.update_canvas_size()
        self.draw_maze()

    def update_canvas_size(self):
        base_size = self.cell_size * max(self.rows, self.cols)
        new_size = int(base_size * self.zoom_level)
        self.canvas.config(width=min(800, new_size), height=min(800, new_size))
        self.canvas.configure(scrollregion=(0, 0, new_size, new_size))

    def draw_maze(self):
        self.canvas.delete('all')
        cell_size = self.cell_size * self.zoom_level
        
        # Desenha o labirinto
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                color = 'white' if self.maze[i][j] == 0 else 'black'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')
        
        # Desenha o agente (ponto inicial)
        ax1 = self.agent_pos[1] * cell_size + cell_size * 0.1
        ay1 = self.agent_pos[0] * cell_size + cell_size * 0.1
        ax2 = ax1 + cell_size * 0.8
        ay2 = ay1 + cell_size * 0.8
        self.canvas.create_oval(ax1, ay1, ax2, ay2, fill='blue')
        
        # Desenha o objetivo (ponto final)
        gx1 = self.goal_pos[1] * cell_size + cell_size * 0.2
        gy1 = self.goal_pos[0] * cell_size + cell_size * 0.2
        gx2 = gx1 + cell_size * 0.6
        gy2 = gy1 + cell_size * 0.6
        self.canvas.create_rectangle(gx1, gy1, gx2, gy2, fill='green')
        
        # Atualiza a região de rolagem
        self.update_canvas_size()

    def generate_batch(self):
        try:
            min_size = int(self.min_size.get())
            max_size = int(self.max_size.get())
            quantity = int(self.quantity.get())
            
            if min_size > max_size:
                messagebox.showerror('Erro', 'Tamanho mínimo deve ser menor que o máximo')
                return
            if min_size < 5:
                messagebox.showerror('Erro', 'Tamanho mínimo deve ser pelo menos 5')
                return
            if quantity < 1:
                messagebox.showerror('Erro', 'Quantidade deve ser maior que 0')
                return
                
            self.batch_mazes = []
            for _ in range(quantity):
                size = random.randint(min_size, max_size)
                self.batch_mazes.append(size)
            
            self.current_batch_index = 0
            self.process_next_batch_maze()
            
        except ValueError:
            messagebox.showerror('Erro', 'Por favor, insira valores numéricos válidos')

    def process_next_batch_maze(self):
        if self.current_batch_index < len(self.batch_mazes):
            size = self.batch_mazes[self.current_batch_index]
            self.rows = size
            self.cols = size
            self.cell_size = min(40, 400 // size)  # Ajusta o tamanho da célula para caber na tela
            self.zoom_level = 1.0  # Reseta o zoom
            self.agent = QLearningAgent(size, size)
            self.generate_maze()
            self.current_batch_index += 1
            self.after(3000, self.process_next_batch_maze)
        else:
            messagebox.showinfo('Info', 'Geração de lotes concluída!')

    def generate_maze(self):
        self.maze = generate_maze(self.rows, self.cols)
        self.agent_pos = (0, 0)
        self.goal_pos = (self.rows-1, self.cols-1)
        self.draw_maze()
        # Treinar agente RL
        self.agent.train(self.maze, (0,0), (self.rows-1, self.cols-1), episodes=5000)
        print(f"Treinamento do agente RL concluído! com os parametros: self.rows = {self.rows} e self.cols = {self.cols}" )
        
        # Executar RL
        rl_start = time.perf_counter()
        rl_path, rl_total_steps = self.agent.get_policy_path_with_steps(self.maze, (0,0), (self.rows-1, self.cols-1))
        rl_time = time.perf_counter() - rl_start
        rl_data = {
            'id_labirinto': self.maze_id,
            'algoritmo': 'RL',
            'tamanho_caminho': len(rl_path),
            'tamanho_labirinto': f'{self.rows}x{self.cols}',
            'total_passos': rl_total_steps,
            'tempo': rl_time,
            'sucesso': rl_path[-1] == (self.rows-1, self.cols-1) if rl_path else False
        }
        
        # Executar Dijkstra
        dj_start = time.perf_counter()
        dj_path, dj_total_steps = dijkstra(self.maze, (0,0), (self.rows-1, self.cols-1))
        dj_time = time.perf_counter() - dj_start
        dj_data = {
            'id_labirinto': self.maze_id,
            'algoritmo': 'Dijkstra',
            'tamanho_caminho': len(dj_path),
            'tamanho_labirinto': f'{self.rows}x{self.cols}',
            'total_passos': dj_total_steps,
            'tempo': dj_time,
            'sucesso': dj_path[-1] == (self.rows-1, self.cols-1) if dj_path else False
        }
        
        # Salvar no results.csv
        fieldnames = ['id_labirinto', 'algoritmo', 'tamanho_caminho', 'tamanho_labirinto', 'total_passos', 'tempo', 'sucesso']
        export_to_csv('results.csv', rl_data, fieldnames)
        export_to_csv('results.csv', dj_data, fieldnames)
        self.maze_id += 1

    def train_agent(self):
        self.agent.train(self.maze, (0,0), (self.rows-1, self.cols-1), episodes=5000)
        messagebox.showinfo('Info', 'Treinamento do agente concluído!')

    def solve_rl(self):
        path, total_steps = self.agent.get_policy_path_with_steps(self.maze, (0,0), (self.rows-1, self.cols-1))
        if len(path) <= 1:
            messagebox.showinfo('Info', 'O agente não encontrou um caminho até o objetivo!')
            return
        self.animate_path(path)

    def animate_path(self, path, delay=150):
        if not path:
            return
        self.agent_pos = path[0]
        self.draw_maze()
        if len(path) > 1:
            self.after(delay, lambda: self.animate_path(path[1:], delay))

    def solve_dijkstra(self):
        path, total_steps = dijkstra(self.maze, (0,0), (self.rows-1, self.cols-1))
        if len(path) <= 1:
            messagebox.showinfo('Info', 'Dijkstra não encontrou um caminho até o objetivo!')
            return
        self.animate_path(path)

    def save_qtable(self):
        filename = filedialog.asksaveasfilename(defaultextension='.qtable', filetypes=[('Q-table files', '*.qtable'), ('All files', '*.*')])
        if filename:
            self.agent.save_qtable(filename)
            messagebox.showinfo('Info', f'Q-table salva em {filename}')

    def load_qtable(self):
        filename = filedialog.askopenfilename(defaultextension='.qtable', filetypes=[('Q-table files', '*.qtable'), ('All files', '*.*')])
        if filename:
            try:
                self.agent.load_qtable(filename)
                messagebox.showinfo('Info', f'Q-table carregada de {filename}')
            except Exception as e:
                messagebox.showerror('Erro', str(e))

    def export_rl_csv(self):
        start_time = time.perf_counter()
        path = self.agent.get_policy_path(self.maze, (0,0), (self.rows-1, self.cols-1))
        elapsed = time.perf_counter() - start_time
        data = {
            'id_labirinto': self.maze_id,
            'algoritmo': 'RL',
            'tamanho_caminho': len(path),
            'tempo': elapsed,
            'sucesso': path[-1] == (self.rows-1, self.cols-1) if path else False
        }
        filename = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
        if filename:
            export_to_csv(filename, data, ['id_labirinto', 'algoritmo', 'tamanho_caminho', 'tempo', 'sucesso'])
            messagebox.showinfo('Info', f'Resultado RL exportado para {filename}')

    def export_dijkstra_csv(self):
        from dijkstra import dijkstra
        start_time = time.perf_counter()
        path = dijkstra(self.maze, (0,0), (self.rows-1, self.cols-1))
        elapsed = time.perf_counter() - start_time
        data = {
            'id_labirinto': self.maze_id,
            'algoritmo': 'Dijkstra',
            'tamanho_caminho': len(path),
            'tempo': elapsed,
            'sucesso': path[-1] == (self.rows-1, self.cols-1) if path else False
        }
        filename = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
        if filename:
            export_to_csv(filename, data, ['id_labirinto', 'algoritmo', 'tamanho_caminho', 'tempo', 'sucesso'])
            messagebox.showinfo('Info', f'Resultado Dijkstra exportado para {filename}')

if __name__ == '__main__':
    app = MazeUI()
    app.mainloop() 