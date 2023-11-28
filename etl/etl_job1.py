import csv
import pandas as pd

# Nome do arquivo CSV original
nome_arquivo_original = 'data/plano_geografico.csv'

# Nome do novo arquivo CSV
nome_arquivo_novo = 'raw_data/plano_geografico_corrigido.csv'

with open(nome_arquivo_original, 'r') as arquivo_original:
    with open(nome_arquivo_novo, 'w') as arquivo_novo:
        leitor = csv.reader(arquivo_original)
        escritor = csv.writer(arquivo_novo)
        for linha in leitor:
            linha = linha[0].split(';')
            linha = [item.replace('"', '').replace("'", '') for item in linha]
            escritor.writerow(linha)

df_plano_geografico = pd.read_csv(nome_arquivo_novo)
df_agrupado = df_plano_geografico.groupby(['ID_PLANO', 'CD_PLANO', 'CD_OPERADORA', 'CD_NOTA', 'DT_NTRP', 'SG_UF', 'NM_REGIAO', 'DT_ATUALIZACAO']).agg({
    'CD_MUNICIPIO': lambda x: list(x),
    'NM_MUNICIPIO_X': lambda x: list(x)
}).reset_index()

df_agrupado.to_csv(nome_arquivo_novo, index=False, mode='w')

print(f"Foi criado um novo arquivo CSV chamado {nome_arquivo_novo} com os dados do arquivo original e agrupamento realizado.")