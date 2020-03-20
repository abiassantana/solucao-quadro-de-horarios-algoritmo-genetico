import matplotlib.pyplot as plt
import pandas as pd
import os
def gerar_grafico_gerações():
    arquivos = os.listdir('geracoes')
    dfs = []
    eixo_x = []
    eixo_y = []
    best = {'numero_geracao': None, 'id': None, 'fitness': float('+inf')}
    for arquivo in arquivos:
        dfs.append(pd.read_csv('geracoes/'+arquivo))
    dfs_sorted = sorted(dfs,key=key)
    for df in dfs_sorted:
        if df.iloc[0]['fitness'] < best['fitness']:
            best['fitness'] = df.iloc[0]['fitness']
            best['numero_geracao'] = df.iloc[0]['numero']
            best['id'] = df.iloc[0]['best_id']
        eixo_x.append(df.iloc[0]['numero'])
        eixo_y.append(df.iloc[0]['fitness'])
    plt.plot(eixo_x, eixo_y)
    plt.title('Grafico valor melhor fitness por gerações')
    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    print(best)
    plt.show()

def key(df):
    return df.iloc[0]['numero']

