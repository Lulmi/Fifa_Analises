import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="Análise de Clubes - FIFA (2017-2023)",
    page_icon="🏟️",
    layout="wide"
)

# ---------------------------- SIDEBAR: FILTROS ---------------------------- #
st.sidebar.title("⚙️ Filtros")

# Definindo o path fixo que você pediu
DATA_DIR = "C:/Users/lucas/OneDrive/Documents/Educação/Asimov_Academy/Criando Aplicativos Web com Streamlit/Projeto Streamlit FIFA/datasets/"

# Lista de anos disponíveis
available_years = ["17", "18", "19", "20", "22", "23"]
year = st.sidebar.selectbox("Selecione o Ano", available_years)

# Montando o nome completo do arquivo
filename = f"CLEAN_FIFA{year}_official_data.csv"
filepath = os.path.join(DATA_DIR, filename)

# ---------------------------- FUNÇÃO PARA CARREGAR OS DADOS ---------------------------- #
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Carregando os dados
df = load_data(filepath)

# ---------------------------- HEADER PRINCIPAL ---------------------------- #
st.title("🏟️ Análise de Clubes - FIFA (2017-2023)")
st.markdown(f"### 📁 Dataset Carregado: `{filename}`")
st.markdown("---")

# ---------------------------- ANÁLISES ---------------------------- #

# Cálculo das médias de overall por clube
club_overall = df.groupby('Club')['Overall'].mean().reset_index().sort_values(by='Overall', ascending=False)
club_counts = df['Club'].value_counts().reset_index()
club_counts.columns = ['Club', 'Number of Players']

# 🏆 Top 10 clubes com maior média de overall
st.subheader("🏆 Top 10 Clubes com Maior Média de Overall")
st.dataframe(club_overall.head(10))

# 🥈 Bottom 10 clubes com menor média de overall
st.subheader("🥈 Bottom 10 Clubes com Menor Média de Overall")
st.dataframe(club_overall.tail(10))

# 📋 Clubes com mais jogadores no dataset
st.subheader("📋 Clubes com Mais Jogadores no Dataset")
st.dataframe(club_counts.head(10))

# 📌 Detalhes dos clubes (média de overall + quantidade de jogadores)
st.subheader("📌 Detalhes dos Clubes (Média de Overall + Quantidade de Jogadores)")
club_details = pd.merge(club_overall, club_counts, on='Club')
st.dataframe(club_details.sort_values(by='Number of Players', ascending=False))

st.markdown("---")

# ---------------------------- SCATTER PLOT: Release Clause vs Overall ---------------------------- #
if 'Release Clause(£)' in df.columns:
    st.subheader("📈 Relação entre Release Clause(£) e Overall dos Jogadores")

    # Tratamento para valores nulos e garantir que Release Clause(£) seja numérico
    df_filtered = df[['Release Clause(£)', 'Overall', 'Club']].dropna()
    df_filtered = df_filtered[df_filtered['Release Clause(£)'] > 0]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df_filtered,
        x='Release Clause(£)',
        y='Overall',
        hue='Club',
        legend=False,
        alpha=0.6
    )
    plt.xlabel('Release Clause(£)')
    plt.ylabel('Overall')
    plt.title('Relação entre Release Clause(£) e Overall')
    plt.xscale('log')  # Melhora a visualização se houver disparidades muito grandes no valor da cláusula
    st.pyplot(fig)
else:
    st.warning("⚠️ A coluna 'Release Clause(£)' não está disponível neste ano de dataset.")

# ---------------------------- FOOTER ---------------------------- #
st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Análise de Dados com FIFA (2017-2023)")
