import streamlit as st
import pandas as pd
import os
import sys

# ---------------------------- AJUSTE DE CAMINHO PARA IMPORTAÇÃO ---------------------------- #
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from load_data import carregar_dados

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
available_years = ["17", "18", "19", "20", "22", "23"]
year = st.sidebar.selectbox("Selecione o Ano", available_years)
ano_completo = int("20" + year) if year != "17" else 2017
df = carregar_dados(ano_completo)

# ---------------------------- ESCOLHA DO ESQUEMA TÁTICO ---------------------------- #
formation_options = {
    "4-3-3": {'GK': 1, 'CB': 2, 'LB': 1, 'RB': 1, 'CDM': 1, 'CM': 2, 'LW': 1, 'RW': 1, 'ST': 1},
    "4-4-2": {'GK': 1, 'CB': 2, 'LB': 1, 'RB': 1, 'CDM': 2, 'CM': 2, 'LW': 1, 'RW': 1, 'ST': 2},
    "3-5-2": {'GK': 1, 'CB': 3, 'CDM': 2, 'CM': 2, 'CAM': 1, 'LW': 1, 'RW': 1, 'ST': 2},
    "4-2-3-1": {'GK': 1, 'CB': 2, 'LB': 1, 'RB': 1, 'CDM': 2, 'CM': 1, 'CAM': 1, 'LW': 1, 'RW': 1, 'ST': 1}
}
formation = st.sidebar.selectbox("Escolha o Esquema Tático", list(formation_options.keys()))
positions_required = formation_options[formation]

budget = st.sidebar.slider("💰 Orçamento Máximo (£ milhões)", 10, 500, 100)

# ---------------------------- TÍTULO ---------------------------- #
st.title("🌟 Dream Team - FIFA (2017-2023)")
st.markdown(f"### 📁 Dataset Carregado: `CLEAN_FIFA{year}_official_data.csv`")
st.markdown(f"### 🧩 Esquema Tático: `{formation}`")
st.markdown("---")

# ---------------------------- FUNÇÃO PARA MONTAR TIME ---------------------------- #
def select_players(criteria, budget_limit=None):
    team = []
    df_team = df.copy()

    if criteria == 'custo_beneficio' and 'release clause(£)' in df_team.columns:
        df_team = df_team[df_team['release clause(£)'] > 0]
        df_team['score_por_liberacao'] = df_team['overall'] / df_team['release clause(£)']
    elif criteria == 'baixo_orcamento' and 'release clause(£)' in df_team.columns:
        df_team = df_team[df_team['release clause(£)'] > 0]

    for pos, qty in positions_required.items():
        players_pos = df_team[df_team['position'].str.contains(pos, na=False)]

        if players_pos.empty:
            continue

        if criteria == 'melhor':
            players_pos = players_pos.sort_values(by='overall', ascending=False)
        elif criteria == 'custo_beneficio':
            players_pos = players_pos.sort_values(by='score_por_liberacao', ascending=False)
        elif criteria == 'baixo_orcamento':
            players_pos = players_pos.sort_values(by='overall', ascending=False)
            players_pos = players_pos[players_pos['release clause(£)'].cumsum() <= budget_limit * 1_000_000]

        team.append(players_pos.head(qty))

    return pd.concat(team) if team else pd.DataFrame()

# ---------------------------- EXIBIR TIME ---------------------------- #
def display_team(title, team_df):
    if team_df.empty:
        st.warning(f"⚠️ Não foi possível montar o time para: {title}")
    else:
        team_df = team_df.copy()
        team_df['overall'] = team_df['overall'].round(2)
        team_df['potential'] = team_df['potential'].round(2)
        if 'release clause(£)' in team_df.columns:
            team_df['release clause(£)'] = team_df['release clause(£)'].apply(format_currency)

        cols = ['name', 'age', 'nationality', 'club', 'position', 'overall', 'potential']
        if 'release clause(£)' in team_df.columns:
            cols.append('release clause(£)')
        st.subheader(title)
        st.dataframe(team_df[cols], use_container_width=True)

# ---------------------------- TIMES ---------------------------- #
display_team("⭐ Melhor Time por Overall", select_players('melhor'))

if 'release clause(£)' in df.columns:
    display_team("💎 Time Custo-Benefício (Overall / Release Clause)", select_players('custo_beneficio'))
    display_team(f"🤑 Time Econômico (até £{budget}M)", select_players('baixo_orcamento', budget_limit=budget))
else:
    st.warning("⚠️ A coluna 'Release Clause(£)' não está disponível neste dataset.")

# ---------------------------- FOOTER ---------------------------- #
st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Dream Team FIFA (2017-2023)")
