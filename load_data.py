import pandas as pd
from pathlib import Path

# ---------------------------- CONFIGURAÇÃO GLOBAL ---------------------------- #
BASE_DIR = Path(__file__).resolve().parent / "datasets"
ANOS = list(range(2017, 2024))
ARQUIVOS = {ano: f"CLEAN_FIFA{str(ano)[-2:]}_official_data.csv" for ano in ANOS}


# ---------------------------- PADRONIZAÇÃO DE NOMES ---------------------------- #
def padronizar_colunas(df):
    # Normaliza nomes com snake_case simplificado
    df.columns = (
        df.columns.str.lower()
        .str.strip()
        .str.replace(" ", "")
        .str.replace("_", "")
    )

    # Mapeamento explícito para garantir consistência
    renomear = {
        'team': 'club',
        'value(€)': 'value_eur',
        'value': 'value_eur',
        'releaseclause(£)': 'release_clause(£)',
    }

    df = df.rename(columns={col: renomear[col] for col in renomear if col in df.columns})

    # Garante que coluna de valor exista
    if 'value_eur' not in df.columns:
        df['value_eur'] = None

    return df


# ---------------------------- FUNÇÃO DE CARREGAMENTO POR ANO ---------------------------- #
def carregar_dados(ano: int) -> pd.DataFrame:
    caminho = BASE_DIR / ARQUIVOS[ano]
    df = pd.read_csv(caminho)
    df = padronizar_colunas(df)
    df['year'] = ano

    colunas_finais = [
        'year', 'name', 'age', 'nationality', 'club', 'position',
        'overall', 'potential', 'value_eur', 'release_clause(£)'
    ]
    return df[[col for col in colunas_finais if col in df.columns]]


# ---------------------------- FUNÇÃO PARA CONCATENAR TODOS ---------------------------- #
def carregar_todos_os_dados() -> pd.DataFrame:
    return pd.concat([carregar_dados(ano) for ano in ANOS], ignore_index=True)
