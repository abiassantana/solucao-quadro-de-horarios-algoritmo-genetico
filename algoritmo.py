from dados_iniciais import gerador_dados_iniciais

class algoritmo:

    gerador_inicial = None

    def __init__(self, periodos, csv_salas, dias, individuos_geracao, hora_aula, 
    qnt_aula_min_x, qnt_aulas_manha, qnt_aulas_tarde, qnt_aulas_noite):
        self.gerador_inicial = gerador_dados_iniciais(periodos, csv_salas,  
        dias, individuos_geracao, hora_aula, qnt_aula_min_x, qnt_aulas_manha, 
        qnt_aulas_tarde, qnt_aulas_noite)
        self.gerador_inicial.gerar_quadros_iniciais()

    def pontuador(self):
        pass

    
    