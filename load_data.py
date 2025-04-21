import pandas as pd
import os

# Caminho para os arquivos
caminho_base = "C:/Users/lucas/OneDrive/Documents/Educação/Asimov_Academy/Criando Aplicativos Web com Streamlit/Projeto Streamlit FIFA/datasets"

# Anos disponíveis
anos = list(range(2017, 2024))

# Usar apenas os dois últimos dígitos no nome do arquivo
nomes_arquivos = {
    ano: f"CLEAN_FIFA{str(ano)[-2:]}_official_data.csv" for ano in anos
}

def carregar_dados(ano):
    caminho = os.path.join(caminho_base, nomes_arquivos[ano])
    df = pd.read_csv(caminho)
    df.columns = [col.lower().strip() for col in df.columns]
    df['year'] = ano

    # Mapeamento de colunas
    col_map = {
        'name': 'name', 'age': 'age', 'nationality': 'nationality',
        'club': 'club', 'team': 'club', 'position': 'position',
        'overall': 'overall', 'potential': 'potential',
        'value(€)': 'value_eur', 'value': 'value_eur'
    }

    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

    # Preenche a coluna de valor com None caso não exista
    if 'value_eur' not in df.columns:
        df['value_eur'] = None

    # Seleciona apenas as colunas desejadas
    colunas_finais = ['year', 'name', 'age', 'nationality', 'club', 'position', 'overall', 'potential', 'value_eur']
    return df[[col for col in colunas_finais if col in df.columns]]

def carregar_todos_os_dados():
    return pd.concat([carregar_dados(ano) for ano in anos], ignore_index=True)