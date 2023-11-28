import pandas as pd
from datetime import date

arquivo_historico = 'data/historico.csv'

# Carregar o arquivo_historico CSV
df_historico = pd.read_csv(arquivo_historico, dtype={"#ID_PLANO": int, "CD_PLANO": "string", "CD_OPERADORA": int, "DT_INICIO_STATUS": "string", "DT_FIM_STATUS": "string", "ID_SITUACAO_PRINCIPAL": int, "DE_SITUACAO_PRINCIPAL":"string"})

# Preencher dados faltantes com base no status
def preencher_dados_data(row):
    if row['DE_SITUACAO_PRINCIPAL'] == 'ATIVO' or row['DE_SITUACAO_PRINCIPAL'] == 'ATIVO COM COMERCIALIZAÇÃO SUSPENSA' and pd.isnull(row['DT_FIM_STATUS']):
        data = date.today()
        data = data.strftime('%d/%m/%Y')
        return data
    elif row['DE_SITUACAO_PRINCIPAL'] == 'CANCELADO' or row['DE_SITUACAO_PRINCIPAL'] == 'TRANSFERIDO' and pd.isnull(row['DT_FIM_STATUS']):
        data_inicio = row['DT_INICIO_STATUS']
        return data_inicio
    else:
        return row['DT_FIM_STATUS']
    
def preencher_dados_cdPlano(row):
    if pd.isnull(row['CD_PLANO']):
        return '0'
    else:
        return row['CD_PLANO']

df_historico['DT_FIM_STATUS'] = df_historico.apply(preencher_dados_data, axis=1)
df_historico['CD_PLANO'] = df_historico.apply(preencher_dados_cdPlano, axis=1)
    
df_historico.to_csv('raw_data/historico_corrigido.csv', index=False)

print("Dados preenchidos e salvos em 'historico_corrigido.csv'.")