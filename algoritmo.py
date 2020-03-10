from dados_iniciais import gerador_dados_iniciais

class algoritmo:

    gerador_inicial = None

    def __init__(self, csv_salas, horarios_csv, cadeiras_csv, tamanho_geracao, requisitos):
        self.tamanho_geracao = tamanho_geracao
        self.gerador_inicial = gerador_dados_iniciais(csv_salas, horarios_csv, cadeiras_csv, self.tamanho_geracao)
        self.populacoes = self.gerador_inicial.gerar_quadros_iniciais()
        self.notas_populaçao_geracoes = {}
        self.requisitos = requisitos
        # print(self.cromosomos)

    def pontuador(self):
        geracao = len(self.populacoes)-1
        self.notas_populaçao_geracoes[geracao] = {}
        for i in self.requisitos:
            for pop in self.populacoes:
                for indv in self.populacoes[pop]:
                    try:
                        self.notas_populaçao_geracoes[geracao][indv] += i(self.populacoes[geracao][indv])
                    except KeyError:
                        self.notas_populaçao_geracoes[geracao][indv] = i(self.populacoes[geracao][indv])
        print(self.notas_populaçao_geracoes)

    
    