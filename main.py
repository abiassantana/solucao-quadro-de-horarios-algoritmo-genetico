from algoritmo import algoritmo
import requisitos as req

requisitos = [req.diciplina_mesmo_p_h, req.professor_mesmo_h, req.diciplina_mesmo_dia]

a = algoritmo('csv/salas.csv', 'csv/horarios.csv', 'csv/cadeiras.csv', 50, requisitos)
print(a.pontuar_individuo(a.populacoes[0][0], True))