import pandas as pd
import random
class gerador_dados_iniciais:

    csv_inicial = {}
    cadeiras = {}
    individuos_geracao = None
    hora_aula = None
    qnt_aula_min_x = None
    qnt_aulas_manha = None
    qnt_aulas_tarde = None
    qnt_aulas_noite = None
    periodos = None
    salas = None
    dias_semana = None

    def __init__(self, periodos, csv_salas, dias, individuos_geracao, hora_aula,
     qnt_aula_min_x, qnt_aulas_manha, qnt_aulas_tarde, qnt_aulas_noite):
        self.periodos = periodos
        self.dias = dias
        self.individuos_geracao = individuos_geracao
        self.hora_aula = hora_aula
        self.qnt_aula_min_x = qnt_aula_min_x
        self.qnt_aulas_manha = qnt_aulas_manha
        self.qnt_aulas_tarde = qnt_aulas_tarde
        self.qnt_aulas_noite = qnt_aulas_noite
        self.salas = self.carregar_csv_salas(csv_salas)
        for p in periodos:
            self.carregar_csv_periodos(p)
        self.tratar_csv()
        
    def carregar_csv_salas(self, salas_csv):
        salas_temp = pd.read_csv(salas_csv)
        salas = {}
        for i, row in salas_temp.iterrows():
            nome, capacidade = row
            salas[nome] = {'capacidade': capacidade}
        return salas

    def carregar_csv_periodos(self, periodo):
        self.csv_inicial[periodo] = pd.read_csv(periodo+'.csv')
    
    def tratar_csv(self):
        for i in self.periodos:
            self.tratar_periodo_csv(i)

    def tratar_periodo_csv(self, periodo):
        self.cadeiras[periodo] = {}
        for i, row in self.csv_inicial[periodo].iterrows():
            nome, codigo, cr, carga_h = row
            self.cadeiras[periodo][codigo]={
                        'nome': nome,
                        'cr': cr,
                        'carga_h': carga_h
                    }

    def gerar_quadros_iniciais(self):
        cadeiras_temp = self.cadeiras.copy()
        cromosomos = []
        for i in cadeiras_temp:
            for r in range(self.individuos_geracao):
                cromosomo = ''
                for dia in self.dias:
                    cromosomo += str(dia)+'|'
                    for e in range(self.qnt_aulas_manha+self.qnt_aulas_tarde+self.qnt_aulas_noite):
                        cadeira_cod = random.choice(list(self.cadeiras[i].keys()))
                        sala_cod = random.choice(list(self.salas.keys()))
                        cromosomo += 'A'+str(e)+':'+str(cadeira_cod)+'%'+sala_cod+';'
                cromosomo += '/'
                print(cromosomo)
    
    def verificar_carga_h(self, cadeiras_periodo, cadeira_cod):
        if cadeiras_periodo[cadeira_cod]['carga_h'] > self.qnt_aula_min_x * self.hora_aula:
            return True
        return False
    

        

