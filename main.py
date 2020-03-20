from algoritmo import algoritmo
import requisitos as req
from util import gerar_grafico_gerações

requisitos = [req.diciplina_mesmo_p_h, req.professor_mesmo_h, req.diciplina_mesmo_dia, req.aulas_concecutivas]
def parar_pop_1000(algoritmo):
    if len(algoritmo.populacoes) == 10:
        return True
    return False

def funcao_parada(algoritmo):
    count = 0
    for indv in algoritmo.populacoes[algoritmo.get_geracao_atual()]:
        if algoritmo.populacoes[algoritmo.get_geracao_atual()][indv]['rate'] < 1000:
            count+=1
        if count >= 1:
            return True
    return False

funcoes_parada = [parar_pop_1000]
cursos = ['lcc','si']
a = algoritmo('csv/salas.csv', 'csv/horarios.csv', 'csv/cadeiras.csv', 2, 50, requisitos, funcoes_parada, 1,cursos)
a.main()
# gerar_grafico_gerações()
