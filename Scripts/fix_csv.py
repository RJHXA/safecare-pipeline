import csv

# Nome do arquivo CSV original
nome_arquivo_original = './plano_geografico.csv'

# Nome do novo arquivo CSV
nome_arquivo_novo = '../raw_data/plano_geografico_corrigido.csv'

with open(nome_arquivo_original, 'r') as arquivo_original:
    with open(nome_arquivo_novo, 'w') as arquivo_novo:
        leitor = csv.reader(arquivo_original)
        escritor = csv.writer(arquivo_novo)
        for linha in leitor:
            linha = linha[0].split(';')
            linha = [item.replace('"', '').replace("'", '') for item in linha]
            escritor.writerow(linha)

print(f"Foi criado um novo arquivo CSV chamado {nome_arquivo_novo} com os dados do arquivo original.")