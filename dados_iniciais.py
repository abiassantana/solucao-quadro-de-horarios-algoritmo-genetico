import pandas as pd
import random
class gerador_dados_iniciais:

    cadeiras = {}
    tamanho_geracao = None
    horarios = []
    salas = []
    

    def __init__(self, salas_csv, horarios_csv, cadeiras_csv, tamanho_geracao):
        self.tamanho_geracao = tamanho_geracao
        self.horarios = self.carregar_csv(horarios_csv)
        self.salas = self.carregar_csv(salas_csv)
        self.cadeiras = self.carregar_csv(cadeiras_csv)
        self.qnt_aulas_semana = 2
        
            
    def carregar_csv(self, csv):
        return pd.read_csv(csv)
    

    def gerar_quadros_iniciais(self):
        cadeiras_temp = self.cadeiras.copy()
        cromosomos = []
        for e in range(self.tamanho_geracao):
            cromosomo = {}
            for i, row in self.cadeiras.iterrows():
                for q in range(self.qnt_aulas_semana):
                    horario = self.horarios.sample(n=1)
                    sala = self.salas.sample(n=1)
                    cromosomo[row['id']] = [
                    sala['codigo'].values[0],
                    row['periodo'],
                    row['professor'],
                    horario['id'].values[0]]
            cromosomos.append(cromosomo)
        return cromosomos