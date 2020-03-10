
def diciplina_mesmo_p_h(indiv):
    for gene in indiv:
        count = 0
        periodo = indiv[gene][1]
        horario = indiv[gene][3]
        for i in indiv:
            if periodo == indiv[i][1] and horario == indiv[i][3]:
                count+=1
                if count >= 2:
                    return float("-inf")
        return 0

def professor_mesmo_h(indiv):
    for gene in indiv:
        count = 0
        prof = indiv[gene][2]
        horario = indiv[gene][3]
        for i in indiv:
            if prof == indiv[i][2] and horario == indiv[i][3]:
                count+=1
                if count >= 2:
                    return float("-inf")
        return 0

def diciplina_mesmo_h(indiv):
    for gene in indiv:
        count = 0
        diciplina = gene
        horario = indiv[gene][3]
        for i in indiv:
            if diciplina == i and horario == indiv[i][3]:
                count+=1
                if count >= 2:
                    print('chamou')
                    return float("-inf")
        return 0

