import streamlit as st
import pandas as pd
import os

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="Dream Team - FIFA (2017-2023)",
    page_icon="🌟",
    layout="wide"
)

# ---------------------------- FUNÇÃO DE FORMATAÇÃO ---------------------------- #
def format_currency(value):
    if pd.isna(value):
        return "-"
    return f"£ {value:,.0f}".replace(",", ".")

# ---------------------------- SIDEBAR ---------------------------- #
st.sidebar.title("⚙️ Configuração do Dream Team")

DATA_DIR = "C:/Users/lucas/OneDrive/Documents/Educação/Asimov_Academy/Criando Aplicativos Web com Streamlit/Projeto Streamlit FIFA/datasets/"
available_years = ["17", "18", "19", "20", "22", "23"]
year = st.sidebar.selectbox("Selecione o Ano", available_years)
filename = f"CLEAN_FIFA{year}_official_data.csv"
filepath = os.path.join(DATA_DIR, filename)

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

df = load_data(filepath)

# ---------------------------- ESCOLHA DO ESQUEMA TÁTICO ---------------------------- #
formation_options = {
    "4-3-3": {'GK': 1, 'CB': 2, 'LB': 1, 'RB': 1, 'CDM': 1, 'CM': 2, 'LW': 1, 'RW': 1, 'ST': 1},
    "4-4-2": {'GK': 1, 'CB': 2, 'LB': 1, 'RB': 1, 'CDM': 2, 'CM': 2, 'LW': 1, 'RW': 1, 'ST': 2},
    "3-5-2": {'GK': 1, 'CB': 3, 'CDM': 2, 'CM': 2, 'CAM': 1, 'LW': 1, 'RW': 1, 'ST': 2},
    "4-2-3-1": {'GK': 1, 'CB': 2, 'LB': 1, 'RB': 1, 'CDM': 2, 'CM': 1, 'CAM': 1, 'LW': 1, 'RW': 1, 'ST': 1}
}

formation = st.sidebar.selectbox("Escolha o Esquema Tático", list(formation_options.keys()))
positions_required = formation_options[formation]

budget = st.sidebar.slider("💰 Defina o Orçamento Máximo (£ milhões) para o Time Econômico", 10, 500, 100)

st.title("🌟 Dream Team - FIFA (2017-2023)")
st.markdown(f"### 📁 Dataset Carregado: `{filename}`")
st.markdown(f"### 🧩 Esquema Tático Selecionado: `{formation}`")
st.markdown("---")

# ---------------------------- FUNÇÕES PARA ESCOLHER O DREAM TEAM ---------------------------- #
def select_players(criteria, budget_limit=None):
    team = []
    df_team = df.copy()

    if criteria == 'custo_beneficio' and 'Release Clause(£)' in df_team.columns:
        df_team = df_team[df_team['Release Clause(£)'] > 0]
        df_team['Score per Pound'] = df_team['Overall'] / df_team['Release Clause(£)']
    elif criteria == 'baixo_orcamento' and 'Release Clause(£)' in df_team.columns:
        df_team = df_team[df_team['Release Clause(£)'] > 0]

    for pos, qty in positions_required.items():
        players_pos = df_team[df_team['Position'].str.contains(pos, na=False)]

        if players_pos.empty:
            continue  # Pula a posição se não houver jogadores

        if criteria == 'melhor':
            players_pos = players_pos.sort_values(by='Overall', ascending=False)
        elif criteria == 'custo_beneficio':
            players_pos = players_pos.sort_values(by='Score per Pound', ascending=False)
        elif criteria == 'baixo_orcamento':
            players_pos = players_pos.sort_values(by='Overall', ascending=False)
            players_pos = players_pos[players_pos['Release Clause(£)'].cumsum() <= budget_limit * 1_000_000]

        team.append(players_pos.head(qty))

    if team:
        return pd.concat(team)
    else:
        return pd.DataFrame()  # Retorna DataFrame vazio se não montar time

# ---------------------------- SELEÇÃO DOS TIMES ---------------------------- #
def display_team(title, team_df):
    if team_df.empty:
        st.warning(f"⚠️ Não foi possível montar o time para: {title}")
    else:
        team_df = team_df.copy()
        team_df['Overall'] = team_df['Overall'].round(2)
        team_df['Potential'] = team_df['Potential'].round(2)

        if 'Release Clause(£)' in team_df.columns:
            team_df['Release Clause(£)'] = team_df['Release Clause(£)'].apply(format_currency)

        # Definindo as colunas que existem no DataFrame
        columns_to_show = ['Name', 'Age', 'Nationality', 'Club', 'Position', 'Overall', 'Potential']
        if 'Release Clause(£)' in team_df.columns:
            columns_to_show.append('Release Clause(£)')

        st.dataframe(team_df[columns_to_show], use_container_width=True)

# Melhor time por Overall
st.subheader("⭐ Melhor Time por Overall (sem considerar preço)")
best_team = select_players(criteria='melhor')
display_team("Melhor Overall", best_team)

# Melhor time custo-benefício
st.subheader("💎 Melhor Time Custo-Benefício (Overall / Release Clause(£))")
if 'Release Clause(£)' in df.columns:
    cost_benefit_team = select_players(criteria='custo_beneficio')
    display_team("Melhor Custo-Benefício", cost_benefit_team)
else:
    st.warning("⚠️ A coluna 'Release Clause(£)' não está disponível neste ano de dataset para calcular custo-benefício.")

# Melhor time de baixo orçamento
st.subheader(f"🤑 Melhor Time Orçamento Baixo (até £{budget}M)")
if 'Release Clause(£)' in df.columns:
    cheap_team = select_players(criteria='baixo_orcamento', budget_limit=budget)
    display_team("Time de Baixo Orçamento", cheap_team)
else:
    st.warning("⚠️ A coluna 'Release Clause(£)' não está disponível neste ano de dataset para calcular orçamento baixo.")

st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Análise de Dados com FIFA (2017-2023)")
