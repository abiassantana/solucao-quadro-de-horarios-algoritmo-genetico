from dados_iniciais import gerador_dados_iniciais
from operator import itemgetter 
import pandas as pd
import random
import os

class algoritmo:

    gerador_inicial = None

    def __init__(self, csv_salas, horarios_csv, cadeiras_csv,qnt_aulas_semana, tamanho_geracao, requisitos, funcao_parada, n_results, cursos):
        self.cursos = cursos
        self.n_results = n_results
        self.funcao_parada = funcao_parada
        self.tamanho_geracao = tamanho_geracao
        self.gerador_inicial = gerador_dados_iniciais(csv_salas, horarios_csv, cadeiras_csv, qnt_aulas_semana, self.tamanho_geracao)
        self.populacoes = self.gerador_inicial.gerar_quadros_iniciais()
        self.notas_populaçao_geracoes = {}
        self.requisitos = requisitos
        self.n_best_generation = {}
        self.best_solution = {'rate': float('+inf')}
        
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

    # def get_melhor_indiv_geracao(self, geracao):
    #     best = {'rate': float('+inf')}
    #     for indv in self.populacoes[geracao]:
    #         if self.populacoes[geracao][indv]['rate'] < best['rate']:
    #             best = self.populacoes[geracao][indv]
    #     del self.populacoes[geracao][indv]['rate']
    #     self.pontuar_individuo(self.populacoes[geracao][indv], True)
    #     return best

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

    def crossover_inicio(self, p1, p2, ponto_crossover,filhos,indv_id):
        count = 0
        for cromo in p1[1]:
                if count <= ponto_crossover:
                    filhos[indv_id][cromo] = p1[1][cromo]
                    count+=1
        for crom in p2[1]:
            if count > ponto_crossover:
                filhos[indv_id][crom] = p2[1][crom]
        return filhos

    def crossover_fim(self, p1, p2, ponto_crossover,filhos,indv_id):
        count = 0
        for cromo in p1[1]:
                if count <= ponto_crossover:
                    filhos[indv_id][cromo] = p2[1][cromo]
                    count+=1
        for crom in p2[1]:
            if count > ponto_crossover:
                filhos[indv_id][crom] = p1[1][crom]
        return filhos
    

    def crossover(self):
        # keys = list(self.n_best_generation[self.get_geracao_atual()].keys())
        winners = self.torneio(50)
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
            cross = [self.crossover_inicio, self.crossover_fim]
            cross[random.randint(0,len(cross)-1)](p1, p2, ponto_crossover,filhos,indv_id)
            # print(len(filhos[indv_id]))
            del filhos[indv_id]['rate']
        # print(len(self.populacoes[self.get_geracao_atual()]))
        return filhos

    def mutacao(self, populacao):
        for indv in populacao:
            gene = random.choice(list(populacao[indv]))
            while gene == 'rate':
                gene = random.choice(list(populacao[indv]))
            # print(populacao[indv][gene])
            cadeira = self.find_key_in_cadeiras(gene)
            horario = self.gerador_inicial.horarios.sample(n=1)
            sala = self.gerador_inicial.salas.sample(n=1)
            new_gene = [
            sala['codigo'].values[0],
            cadeira['periodo'],
            cadeira['professor'],
            horario['id'].values[0],
            horario['dia'].values[0],
            populacao[indv][gene][0][5],
            populacao[indv][gene][0][6]]
            tamanho_gene = len(populacao[indv][gene])
            populacao[indv][gene][random.randint(0,tamanho_gene-1)] = new_gene

    def find_key_in_cadeiras(self, key):
        for i, row in self.gerador_inicial.cadeiras.iterrows():
            if row['id'] == key:
                return row
        return None

    def new_generation(self, populacao):
        self.populacoes[self.get_geracao_atual()+1] = populacao
        # p = populacao.copy()
        # self.pontuar_populacao(p, False)

    def get_n_bests(self, populacao, n):
        sorted_pop = sorted(populacao.items(), key = self.key, reverse = False)
        bests = []
        for indv in sorted_pop:
            bests.append(indv)
        return bests[:n]

    def find_key_populacao(self, populacao, individuo):
        keys = populacao.keys()
        for k in keys:
            # print(populacao[k])
            if populacao[k] == individuo:
                return k
        return None

    def relatorio_geracao(self, populacao):
        best = populacao[self.get_n_bests(populacao, 1)[0][0]].copy()
        key = self.find_key_populacao(populacao, best)
        del best['rate']
        best['rate'] = self.pontuar_individuo(best, True)
        dados = {'numero': [self.get_geracao_atual()], 'best_id': [key], 'fitness': [best['rate']]}
        df = pd.DataFrame(data=dados)
        df.to_csv('geracoes/relatorio_geracao_'+str(self.get_geracao_atual())+'.csv', index=False)
        return {'best': best, 'id': key}

    def funcao_parada_principal(self):
        for f in self.funcao_parada:
            if f(self):
                return True
        return False

    def main(self):
        sair = False
        while not sair:
            self.fitness_populacao_atual()
            print('Geração atual: '+str(self.get_geracao_atual()))
            print('Relatorio melhor individuo: ')
            best = self.relatorio_geracao(self.populacoes[self.get_geracao_atual()])
            print('ID do melhor indiviuo da geração: '+str(best['id'])+', fitness melhor individuo: '+str(best['best']['rate']))
            if best['best']['rate'] <= self.best_solution['rate']:
                self.best_solution = best['best'].copy()
            if self.funcao_parada_principal():
                sair = True
            else:
                crosover = self.crossover()
                self.mutacao(crosover)
                self.new_generation(crosover)
        print('Objetivo de quadros atingidos. Resultados foram exportados para pasta resultados')
        print('fitness melhor individuo em todas gerações: '+str(self.best_solution['rate']))
        self.gerar_df_best()
        self.conver_result_csvs(self.get_n_bests(self.populacoes[self.get_geracao_atual()], self.n_results))

    def gerar_df_best(self):
        cursos = {}
        for c in self.cursos:
            cursos[c] = {'codigo_cadeira':[],'nome': [], 'periodo':[], 'professor':[], 'horario':[], 'dia':[]}
        for gene in self.best_solution:
            if gene != 'rate':
                for g in self.best_solution[gene]:
                    # print(g)
                    for i in g[6]:
                        horario = self.find_key_in_horarios(g[3])
                        cursos[i]['codigo_cadeira'].append(gene)
                        cursos[i]['periodo'].append(g[1])
                        cursos[i]['professor'].append(g[2])
                        cursos[i]['horario'].append(horario['hora'])
                        cursos[i]['dia'].append(g[4])
                        cursos[i]['nome'].append(g[5])
        for i in cursos:
            df = pd.DataFrame(data=cursos[i])
            try:
                df.to_csv('best_resultado_'+str(i)+'/best_resultado_'+str(i)+'.csv', index=False)
            except FileNotFoundError:
                os.mkdir('best_resultado_'+str(i))
                df.to_csv('best_resultado_'+str(i)+'/best_resultado_'+str(i)+'.csv', index=False)

    def find_key_in_horarios(self, key):
        for i, row in self.gerador_inicial.horarios.iterrows():
            if row['id'] == key:
                return row
        return None

    def conver_result_csvs(self, populacao):
        cursos = {}
        for c in self.cursos:
            cursos[c] = {'codigo_cadeira':[],'nome': [], 'periodo':[], 'professor':[], 'horario':[], 'dia':[]}
        for indv in populacao:
            for gene in indv[1]:
                if gene != 'rate':
                    for g in indv[1][gene]:
                        # print(g)
                        for i in g[6]:
                            horario = self.find_key_in_horarios(g[3])
                            cursos[i]['codigo_cadeira'].append(gene)
                            cursos[i]['periodo'].append(g[1])
                            cursos[i]['professor'].append(g[2])
                            cursos[i]['horario'].append(horario['hora'])
                            cursos[i]['dia'].append(g[4])
                            cursos[i]['nome'].append(g[5])
            for i in cursos:
                df = pd.DataFrame(data=cursos[i])
                try:
                    df.to_csv('resultados_'+str(i)+'/resultado_'+str(indv[0])+'.csv', index=False)
                except FileNotFoundError:
                    os.mkdir('./resultados_'+str(i))
                    df.to_csv('resultados_'+str(i)+'/resultado_'+str(indv[0])+'.csv', index=False)
        


        

        

    

            

        
    


    
    