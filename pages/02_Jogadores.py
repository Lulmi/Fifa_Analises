import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="Análise de Jogadores - FIFA (2017-2023)",
    page_icon="⚽",
    layout="wide"
)

# ---------------------------- SIDEBAR: FILTROS ---------------------------- #
st.sidebar.title("⚙️ Filtros")

DATA_DIR = "C:/Users/lucas/OneDrive/Documents/Educação/Asimov_Academy/Criando Aplicativos Web com Streamlit/Projeto Streamlit FIFA/datasets/"
available_years = ["17", "18", "19", "20", "22", "23"]
year = st.sidebar.selectbox("Selecione o Ano", available_years)

filename = f"CLEAN_FIFA{year}_official_data.csv"
filepath = os.path.join(DATA_DIR, filename)

# ---------------------------- FUNÇÃO PARA CARREGAR DADOS ---------------------------- #
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

df = load_data(filepath)

# ---------------------------- HEADER PRINCIPAL ---------------------------- #
st.title("⚽ Análise de Jogadores - FIFA (2017-2023)")
st.markdown(f"### 📁 Dataset Carregado: `{filename}`")
st.markdown("---")

# ---------------------------- ANÁLISES DE JOGADORES ---------------------------- #

# 🏆 Top 10 jogadores com maior overall
st.subheader("🏆 Top 10 Jogadores com Maior Overall")
top_players = df[['Name', 'Age', 'Nationality', 'Club', 'Position', 'Overall', 'Potential']].sort_values(by='Overall', ascending=False).head(10)
top_players['Overall'] = top_players['Overall'].round(2)
top_players['Potential'] = top_players['Potential'].round(2)
st.dataframe(top_players, use_container_width=True)

# 🥈 Bottom 10 jogadores com menor overall (mas excluindo jogadores sem clube ou Overall zero, se houver)
st.subheader("🥈 Bottom 10 Jogadores com Menor Overall")
bottom_players = df[['Name', 'Age', 'Nationality', 'Club', 'Position', 'Overall', 'Potential']].sort_values(by='Overall', ascending=True)
bottom_players = bottom_players[bottom_players['Overall'] > 0].head(10)
bottom_players['Overall'] = bottom_players['Overall'].round(2)
bottom_players['Potential'] = bottom_players['Potential'].round(2)
st.dataframe(bottom_players, use_container_width=True)

# 📋 Países com mais jogadores no dataset
st.subheader("📋 Países com Mais Jogadores no Dataset")
country_counts = df['Nationality'].value_counts().reset_index()
country_counts.columns = ['Country', 'Number of Players']
st.dataframe(country_counts.head(10), use_container_width=True)

# 📌 Detalhes dos jogadores (potencial + overall + idade)
st.subheader("📌 Detalhes dos Jogadores (Overall, Potencial, Idade)")
player_details = df[['Name', 'Age', 'Nationality', 'Club', 'Position', 'Overall', 'Potential']].copy()
player_details['Overall'] = player_details['Overall'].round(2)
player_details['Potential'] = player_details['Potential'].round(2)
st.dataframe(player_details.sort_values(by='Potential', ascending=False), use_container_width=True)

st.markdown("---")

# ---------------------------- SCATTER PLOT: Potential vs Overall ---------------------------- #
st.subheader("📈 Relação entre Potential e Overall dos Jogadores")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x='Potential',
    y='Overall',
    hue='Age',
    palette='viridis',
    alpha=0.6
)
plt.xlabel('Potential')
plt.ylabel('Overall')
plt.title('Relação entre Potential e Overall dos Jogadores')
st.pyplot(fig)

# ---------------------------- SCATTER PLOT: Release Clause vs Overall ---------------------------- #
if 'Release Clause(£)' in df.columns:
    st.subheader("💸 Relação entre Release Clause (£) e Overall dos Jogadores")

    # Tratamento para valores nulos e cláusulas iguais a zero
    df_release = df[['Release Clause(£)', 'Overall', 'Name', 'Age', 'Nationality', 'Club']].dropna()
    df_release = df_release[df_release['Release Clause(£)'] > 0]

    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = sns.scatterplot(
        data=df_release,
        x='Release Clause(£)',
        y='Overall',
        hue='Age',
        palette='coolwarm',
        alpha=0.6
    )
    plt.xscale('log')  # Escala logarítmica para melhorar a leitura
    plt.xlabel('Release Clause (£)')
    plt.ylabel('Overall (Score)')
    plt.title('💸 Release Clause (£) vs Overall (Score) dos Jogadores')
    plt.legend(title='Idade', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)
else:
    st.warning("⚠️ A coluna 'Release Clause' não está disponível neste ano de dataset.")


# ---------------------------- FOOTER ---------------------------- #
st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Análise de Dados com FIFA (2017-2023)")
