from dados_iniciais import gerador_dados_iniciais
from operator import itemgetter 
import random

class algoritmo:

    gerador_inicial = None

    def __init__(self, csv_salas, horarios_csv, cadeiras_csv, tamanho_geracao, requisitos, total_generations):
        self.total_generations = total_generations
        self.tamanho_geracao = tamanho_geracao
        self.gerador_inicial = gerador_dados_iniciais(csv_salas, horarios_csv, cadeiras_csv, self.tamanho_geracao)
        self.populacoes = self.gerador_inicial.gerar_quadros_iniciais()
        self.notas_populaçao_geracoes = {}
        self.requisitos = requisitos
        self.n_best_generation = {}
        self.main(self.total_generations)
        
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
        self.pontuar_populacao(self.populacoes[self.get_geracao_atual()], False)

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


    def crossover(self):
        # keys = list(self.n_best_generation[self.get_geracao_atual()].keys())
        winners = self.torneio(5)
        filhos = {}
        for i in range(self.tamanho_geracao):
            p1 = winners[random.randint(0,len(winners)-1)]
            p2 = winners[random.randint(0,len(winners)-1)]
            while p1 == p2:
                p2 = winners[random.randint(0,len(winners)-1)]
            ponto_crossover = random.randint(1,len(p1[1]))
            count = 0
            # print(p1[1])
            indv_id = len(filhos)
            filhos[indv_id] = {}
            for cromo in p1[1]:
                if count <= ponto_crossover:
                    filhos[indv_id][cromo] = p1[1][cromo]
                    count+=1
            for crom in p2[1]:
                if count > ponto_crossover:
                    filhos[indv_id][crom] = p2[1][crom]
            # print(len(filhos[indv_id]))
            del filhos[indv_id]['rate']
        # print(len(self.populacoes[self.get_geracao_atual()]))
        return filhos

    def mutacao(self, populacao):
        for indv in populacao:
            gene = random.choice(list(populacao[indv]))
            while gene == 'rate':
                gene = random.choice(list(populacao[indv]))
            cadeira = self.find_key_in_cadeiras(gene)
            horario = self.gerador_inicial.horarios.sample(n=1)
            sala = self.gerador_inicial.salas.sample(n=1)
            new_gene = [
            sala['codigo'].values[0],
            cadeira['periodo'],
            cadeira['professor'],
            horario['id'].values[0],
            horario['dia'].values[0]]
            tamanho_gene = len(populacao[indv][gene])
            populacao[indv][gene][random.randint(0,tamanho_gene-1)] = new_gene

    def find_key_in_cadeiras(self, key):
        for i, row in self.gerador_inicial.cadeiras.iterrows():
            if row['id'] == key:
                return row
        return None

    def new_generation(self, populacao):
        self.populacoes[self.get_geracao_atual()+1] = populacao

    def get_n_bests(self, populacao, n):
        sorted_pop = sorted(populacao.items(), key = self.key, reverse = False)
        bests = []
        for indv in sorted_pop:
            bests.append(indv)
        return bests[:5]

    def main(self, total_generations):
        sair = False
        while not sair:
            self.fitness_populacao_atual()
            crosover = self.crossover()
            self.mutacao(crosover)
            self.new_generation(crosover)
            if self.get_geracao_atual() >= total_generations:
                sair = True
        print(self.get_n_bests(self.populacoes[self.get_geracao_atual()-1], 5))
        
        

        

    

            

        
    


    
    