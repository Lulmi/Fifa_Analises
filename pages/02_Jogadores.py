import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# ---------------------------- AJUSTE DE CAMINHO PARA IMPORTAÇÃO ---------------------------- #
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from load_data import carregar_dados

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="Análise de Jogadores - FIFA (2017-2023)",
    page_icon="⚽",
    layout="wide"
)

# ---------------------------- SIDEBAR: FILTROS ---------------------------- #
st.sidebar.title("⚙️ Filtros")
available_years = ["17", "18", "19", "20", "22", "23"]
year = st.sidebar.selectbox("Selecione o Ano", available_years)
ano_completo = int("20" + year) if year != "17" else 2017

# ---------------------------- CARREGAMENTO DE DADOS ---------------------------- #
df = carregar_dados(ano_completo)

# ---------------------------- HEADER ---------------------------- #
st.title("⚽ Análise de Jogadores - FIFA (2017-2023)")
st.markdown(f"### 📁 Dataset Carregado: `CLEAN_FIFA{year}_official_data.csv`")
st.markdown("---")

# ---------------------------- ANÁLISES DE JOGADORES ---------------------------- #

# 🏆 Top 10 jogadores com maior overall
st.subheader("🏆 Top 10 Jogadores com Maior Overall")
top_players = df[['name', 'age', 'nationality', 'club', 'position', 'overall', 'potential']].sort_values(
    by='overall', ascending=False).head(10)
st.dataframe(top_players, use_container_width=True)

# 🥈 Bottom 10 jogadores com menor overall (excluindo Overall = 0)
st.subheader("🥈 Bottom 10 Jogadores com Menor Overall")
bottom_players = df[df['overall'] > 0][['name', 'age', 'nationality', 'club', 'position', 'overall', 'potential']]\
    .sort_values(by='overall').head(10)
st.dataframe(bottom_players, use_container_width=True)

# 📋 Países com mais jogadores
st.subheader("📋 Países com Mais Jogadores no Dataset")
country_counts = df['nationality'].value_counts().reset_index()
country_counts.columns = ['Country', 'Number of Players']
st.dataframe(country_counts.head(10), use_container_width=True)

# 📌 Detalhes completos dos jogadores
st.subheader("📌 Detalhes dos Jogadores (Overall, Potencial, Idade)")
player_details = df[['name', 'age', 'nationality', 'club', 'position', 'overall', 'potential']]
st.dataframe(player_details.sort_values(by='potential', ascending=False), use_container_width=True)

st.markdown("---")

# ---------------------------- SCATTER PLOT: Potential vs Overall ---------------------------- #
st.subheader("📈 Relação entre Potential e Overall dos Jogadores")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x='potential',
    y='overall',
    hue='age',
    palette='viridis',
    alpha=0.6,
    ax=ax
)
plt.xlabel('Potential')
plt.ylabel('Overall')
plt.title('Potential vs Overall')
st.pyplot(fig)

# ---------------------------- SCATTER PLOT: Release Clause vs Overall ---------------------------- #
if 'release clause(£)' in df.columns:
    st.subheader("💸 Relação entre Release Clause (£) e Overall dos Jogadores")

    df_release = df[['release clause(£)', 'overall', 'age']].dropna()
    df_release = df_release[df_release['release clause(£)'] > 0]

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df_release,
        x='release clause(£)',
        y='overall',
        hue='age',
        palette='coolwarm',
        alpha=0.6,
        ax=ax2
    )
    plt.xscale('log')
    plt.xlabel('Release Clause (£)')
    plt.ylabel('Overall')
    plt.title('Release Clause vs Overall')
    st.pyplot(fig2)
else:
    st.warning("⚠️ A coluna 'Release Clause(£)' não está disponível neste ano de dataset.")

# ---------------------------- FOOTER ---------------------------- #
st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Análise de Dados com FIFA (2017-2023)")
