import re

# verifica se exitem aulas de disciplinas
# do mesmo período no mesmo dia e horário 
# caso encontre retorna infinito
def diciplina_mesmo_p_h(indiv, avisos):
    rate = 0
    peso = 1000
    for gene in indiv:
        for aula in indiv[gene]:
            periodo = aula[1]
            horario = aula[3]
            dia = aula[4]
            for i in indiv:
                count = 0
                for au in indiv[i]:
                    if periodo == au[1] and horario == au[3] and dia == au[4] or periodo == au[1] and indiv[i][0][3] == indiv[i][1][3] and indiv[i][0][4] == indiv[i][1][3]:
                        count+=1
                        if count >= 2 and gene != i:
                            rate += peso
                            if avisos:
                                print('Alocações com disciplinas do mesmo período no mesmo dia e hora (custo = '+str(peso)+')')
                                print('- disciplina: '+str(i)+', período: '+str(au[1])+
                                ', dia: '+au[4]+', horário: '+au[3]+', professor: '+au[2])
                                print('- disciplina: '+str(gene)+', período: '+str(periodo)+
                                ', dia: '+aula[4]+', horário: '+horario+', professor: '+aula[2])       
    return rate

# verifica se exitem aulas de disciplinas do mesmo
# professor no mesmo dia e horário 
def professor_mesmo_h(indiv, avisos):
    rate = 0
    peso = 1000
    for gene in indiv:
        for aula in indiv[gene]:
            professor = aula[2]
            horario = aula[3]
            dia = aula[4]
            for i in indiv:
                count = 0
                for au in indiv[i]:
                    if professor == au[1] and horario == au[3] and dia == au[4] or professor == au[1] and indiv[i][0][3] == indiv[i][1][3] and indiv[i][0][4] == indiv[i][1][3]:
                        count+=1
                        if count >= 2 and gene != i:
                            rate += peso
                            if avisos:
                                print('Alocações com disciplinas com professor no mesmo dia e hora (custo = '+str(peso)+')')
                                print('- disciplina: '+str(i)+', período: '+str(au[1])+
                                ', dia: '+au[4]+', horário: '+au[3]+', professor: '+au[2])
                                print('- disciplina: '+str(gene)+', período: '+str(periodo)+
                                ', dia: '+aula[4]+', horário: '+horario+', professor: '+aula[2])
    # print(indiv)       
    return rate

# verifica se exitem aulas da mesma
# disciplina no mesmo dia
def diciplina_mesmo_dia(indiv, avisos):
    peso = 10
    rate = 0
    for gene in indiv:
        for aula in indiv[gene]:
            disciplina = gene
            horario = aula[3]
            dia = aula[4]
            for i in indiv:
                count = 0
                for au in indiv[i]:
                    if disciplina == i and dia == au[4]:
                        count+=1
                        if count >= 2 and gene != i:
                            rate += peso
                            if avisos:
                                print('Alocações com disciplinas com professor no mesmo dia e hora (custo = '+str(peso)+')')
                                print('- disciplina: '+str(i)+', período: '+str(au[1])+
                                ', dia: '+au[4]+', horário: '+au[3]+', professor: '+au[2])
                                print('- disciplina: '+str(gene)+', período: '+str(periodo)+
                                ', dia: '+aula[4]+', horário: '+horario+', professor: '+aula[2])
    return rate


def aulas_concecutivas(indiv, avisos):
    peso = 10
    rate = 0
    for gene in indiv:
        for g in indiv[gene]:
            for gen in indiv:
                for ge in indiv[gene]:
                    horario1 = int(re.sub('[^0-9]', '', g[3]))
                    horario2 = int(re.sub('[^0-9]', '', ge[3]))
                    if gen == gene and horario1 == horario2+1 and g[4] == ge[4]:
                        rate+=peso
                        if avisos:
                            print('Alocações com disciplinas em horarios consecutivas (custo = '+str(peso)+')')
                            print('- disciplina: '+str(gene)+', período: '+str(g[1])+
                                ', dia: '+g[4]+', horário: '+g[3]+', professor: '+g[2])
                            print('- disciplina: '+str(gen)+', período: '+str(g[1])+
                                ', dia: '+ge[4]+', horário: '+ge[3]+', professor: '+ge[2])
    return rate
