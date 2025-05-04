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
    page_title="Análise de Clubes - FIFA (2017-2023)",
    page_icon="🏟️",
    layout="wide"
)

# ---------------------------- SIDEBAR: FILTROS ---------------------------- #
st.sidebar.title("⚙️ Filtros")
available_years = ["17", "18", "19", "20", "22", "23"]
year = st.sidebar.selectbox("Selecione o Ano", available_years)
ano_completo = int("20" + year) if year != "17" else 2017

# ---------------------------- CARREGAMENTO DE DADOS ---------------------------- #
df = carregar_dados(ano_completo)

# ---------------------------- HEADER PRINCIPAL ---------------------------- #
st.title("🏟️ Análise de Clubes - FIFA (2017-2023)")
st.markdown(f"### 📁 Dataset Carregado: `CLEAN_FIFA{year}_official_data.csv`")
st.markdown("---")

# ---------------------------- ANÁLISES DE CLUBES ---------------------------- #
club_overall = df.groupby('club')['overall'].mean().reset_index().sort_values(by='overall', ascending=False)
club_counts = df['club'].value_counts().reset_index()
club_counts.columns = ['club', 'number_of_players']

# 🏆 Top 10 clubes com maior média de overall
st.subheader("🏆 Top 10 Clubes com Maior Média de Overall")
st.dataframe(club_overall.head(10), use_container_width=True)

# 🥈 Bottom 10 clubes com menor média de overall
st.subheader("🥈 Bottom 10 Clubes com Menor Média de Overall")
st.dataframe(club_overall.tail(10), use_container_width=True)

# 📋 Clubes com mais jogadores no dataset
st.subheader("📋 Clubes com Mais Jogadores no Dataset")
st.dataframe(club_counts.head(10), use_container_width=True)

# 📌 Detalhes dos clubes (média de overall + quantidade de jogadores)
st.subheader("📌 Detalhes dos Clubes (Média de Overall + Quantidade de Jogadores)")
club_details = pd.merge(club_overall, club_counts, on='club')
st.dataframe(club_details.sort_values(by='number_of_players', ascending=False), use_container_width=True)

st.markdown("---")

# ---------------------------- SCATTER PLOT: Release Clause vs Overall ---------------------------- #
if 'release clause(£)' in df.columns:
    st.subheader("📈 Relação entre Release Clause(£) e Overall dos Jogadores")

    df_filtered = df[['release clause(£)', 'overall', 'club']].dropna()
    df_filtered = df_filtered[df_filtered['release clause(£)'] > 0]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df_filtered,
        x='release clause(£)',
        y='overall',
        hue='club',
        legend=False,
        alpha=0.6
    )
    plt.xlabel('Release Clause (£)')
    plt.ylabel('Overall')
    plt.title('Relação entre Release Clause(£) e Overall')
    plt.xscale('log')
    st.pyplot(fig)
else:
    st.warning("⚠️ A coluna 'Release Clause(£)' não está disponível neste ano de dataset.")

# ---------------------------- FOOTER ---------------------------- #
st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Análise de Dados com FIFA (2017-2023)")
