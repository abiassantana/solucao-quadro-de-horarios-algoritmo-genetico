from dados_iniciais import gerador_dados_iniciais
from operator import itemgetter 
import random

class algoritmo:

    gerador_inicial = None

    def __init__(self, csv_salas, horarios_csv, cadeiras_csv, tamanho_geracao, requisitos):
        self.tamanho_geracao = tamanho_geracao
        self.gerador_inicial = gerador_dados_iniciais(csv_salas, horarios_csv, cadeiras_csv, self.tamanho_geracao)
        self.populacoes = self.gerador_inicial.gerar_quadros_iniciais()
        self.notas_populaçao_geracoes = {}
        self.requisitos = requisitos
        self.n_best_generation = {}
        self.torneio(5)
        self.crossover()
        # print(self.cromosomos)

    def pontuar_individuo(self, individuo, avisos):
        geracao = len(self.populacoes)-1
        self.notas_populaçao_geracoes[geracao] = {}
        rate = 0
        for i in self.requisitos:
            rate += i(individuo, avisos)
        return rate

    def pontuar_populacao(self, populacao, avisos):
        for indv in populacao:
            rate_indv = self.pontuar_individuo(populacao[indv], avisos)
            populacao[indv]['rate'] = rate_indv

    def fitness_populacao_atual(self):
        self.pontuar_populacao(self.populacoes[len(self.populacoes)-1], False)

    def carregar_quadro_csv(self,csv):
            quadro_csv = self.gerador_inicial.carregar_csv(csv)
            quadro = {}
            for i, row in quadro_csv.iterrows():
                sala = None
                periodo = row['periodo']
                professor = row['professor']
                horario1 = row['horario1']
                dia1 = row['dia1']
                horario2 =row['horario2']
                dia2 = row['dia2']
                quadro[row['id']] = [[sala,periodo,professor,horario1,dia1],[sala,periodo,professor,horario2,dia2]]
            return quadro

    def get_geracao_atual(self):
        return len(self.populacoes)-1

    def key(self,dic):
        return dic[1]['rate']

    def torneio(self, t):
        self.fitness_populacao_atual()
        # dict_sorted = sorted(self.populacoes[self.get_geracao_atual()].items(), key = self.key, reverse = False)
        # print(dict_sorted)
        winners = []
        for i in range(self.tamanho_geracao):
            indivs_torneio_keys = random.sample(list(self.populacoes[self.get_geracao_atual()]), t)
            indivs_torneio = {}
            for e in indivs_torneio_keys:
                indivs_torneio[e] = self.populacoes[self.get_geracao_atual()][e]
            dict_sorted = sorted(indivs_torneio.items(), key = self.key, reverse = False)
            winners.append(dict_sorted[0])
        return winners

        # n_best = {}
        # count = 0
        # for i in range(n):
        #     n_best[dict_sorted[i][0]] =  dict_sorted[i][1]
        # self.n_best_generation[self.get_geracao_atual] = n_best

    def crossover(self):
        # keys = list(self.n_best_generation[self.get_geracao_atual()].keys())
        winners = self.torneio(5)
        
        
    


    
    