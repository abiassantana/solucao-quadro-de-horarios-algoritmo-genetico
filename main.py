from algoritmo import algoritmo
import requisitos as req

requisitos = [req.diciplina_mesmo_p_h, req.professor_mesmo_h, req.diciplina_mesmo_h]

a = algoritmo('csv/salas.csv', 'csv/horarios.csv', 'csv/cadeiras.csv', 100, requisitos)
a.pontuador()