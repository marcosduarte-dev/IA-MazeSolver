import csv
import time

def export_to_csv(filename, data, fieldnames):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

# Exemplo de uso:
if __name__ == '__main__':
    data = {
        'algoritmo': 'RL',
        'tamanho_caminho': 15,
        'tempo': 0.123,
        'sucesso': True
    }
    export_to_csv('resultados.csv', data, ['algoritmo', 'tamanho_caminho', 'tempo', 'sucesso']) 