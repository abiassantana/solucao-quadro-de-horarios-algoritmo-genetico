from algoritmo import algoritmo
import requisitos as req

requisitos = [req.diciplina_mesmo_p_h, req.professor_mesmo_h, req.diciplina_mesmo_dia]

a = algoritmo('csv/salas.csv', 'csv/horarios.csv', 'csv/cadeiras.csv', 50, requisitos)
a.fitness_populacao_atual()
# quadro = a.carregar_quadro_csv('csv/quadro_semestre_si.csv')
# print(a.pontuar_individuo(quadro,True))