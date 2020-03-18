from algoritmo import algoritmo
import requisitos as req

requisitos = [req.diciplina_mesmo_p_h, req.professor_mesmo_h, req.diciplina_mesmo_dia, req.aulas_concecutivas]

def funcao_parada(populacao):
    count = 0
    for indv in populacao:
        if populacao[indv]['rate'] == 0:
            count+=1
        if count >= 1:
            return True
    return False

a = algoritmo('csv/salas.csv', 'csv/horarios.csv', 'csv/cadeiras.csv', 50, requisitos, funcao_parada, 4)
a.main()