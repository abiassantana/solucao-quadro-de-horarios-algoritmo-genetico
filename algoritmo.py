from dados_iniciais import gerador_dados_iniciais

class algoritmo:

    gerador_inicial = None

    def __init__(self, csv_salas, horarios_csv, cadeiras_csv, tamanho_geracao):
        self.tamanho_geracao = tamanho_geracao
        self.gerador_inicial = gerador_dados_iniciais(csv_salas, horarios_csv, cadeiras_csv, self.tamanho_geracao)
        self.cromosomos = self.gerador_inicial.gerar_quadros_iniciais()
        print(self.cromosomos)

    def pontuador(self):
        pass

    
    