import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="Análise por Nacionalidade - FIFA (2017-2023)",
    page_icon="🗺️",
    layout="wide"
)

# ---------------------------- CARREGAMENTO DO DATASET ---------------------------- #
DATA_DIR = "C:/Users/lucas/OneDrive/Documents/Educação/Asimov_Academy/Criando Aplicativos Web com Streamlit/Projeto Streamlit FIFA/datasets/"
available_years = ["17", "18", "19", "20", "22", "23"]
year = st.sidebar.selectbox("Selecione o Ano", available_years)
filename = f"CLEAN_FIFA{year}_official_data.csv"
filepath = os.path.join(DATA_DIR, filename)

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

df = load_data(filepath)

# ---------------------------- CONFIGURAÇÕES INICIAIS ---------------------------- #
st.title("🗺️ Análise por Nacionalidade - FIFA (2017-2023)")
st.markdown(f"### 📁 Dataset Carregado: `{filename}`")
st.markdown("---")

# ---------------------------- MAPA MUNDI: QUANTIDADE DE JOGADORES POR PAÍS ---------------------------- #
st.subheader("🌍 Distribuição de Jogadores por Nacionalidade (Mapa Interativo)")

country_counts = df['Nationality'].value_counts().reset_index()
country_counts.columns = ['Country', 'Number of Players']

fig_map = px.choropleth(
    country_counts,
    locations='Country',
    locationmode='country names',
    color='Number of Players',
    color_continuous_scale='Blues',
    title='Quantidade de Jogadores por País'
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")

# ---------------------------- MAPA MUNDI: MÉDIA DE OVERALL POR PAÍS ---------------------------- #
st.subheader("🌍 Média de Overall por Nacionalidade (Mapa Interativo)")

# Calcula a média de Overall por nacionalidade
overall_avg = df.groupby('Nationality')['Overall'].mean().reset_index()
overall_avg.columns = ['Country', 'Average Overall']

fig_avg_map = px.choropleth(
    overall_avg,
    locations='Country',
    locationmode='country names',
    color='Average Overall',
    color_continuous_scale='Viridis',
    title='Média de Overall por País'
)
st.plotly_chart(fig_avg_map, use_container_width=True)

# ---------------------------- GRÁFICO DE BARRAS: MÉDIA DE OVERALL E POTENTIAL POR NACIONALIDADE ---------------------------- #
st.subheader("📊 Média de Overall e Potential por Nacionalidade (Top 15 Países)")

overall_potential_avg = df.groupby('Nationality')[['Overall', 'Potential']].mean().reset_index()
top_15 = df['Nationality'].value_counts().head(15).index
overall_potential_avg = overall_potential_avg[overall_potential_avg['Nationality'].isin(top_15)]

fig, ax = plt.subplots(figsize=(12, 6))
overall_plot = sns.barplot(data=overall_potential_avg.melt(id_vars='Nationality', value_vars=['Overall', 'Potential']),
                           x='Nationality', y='value', hue='variable', ax=ax)
plt.title('Média de Overall e Potential por Nacionalidade (Top 15)')
plt.ylabel('Média')
plt.xlabel('Nacionalidade')
plt.xticks(rotation=45)
st.pyplot(fig)

st.markdown("---")

# ---------------------------- TOP 5 NACIONALIDADES COM JOGADORES ACIMA DE X OVERALL ---------------------------- #
st.subheader("🏆 Top 5 Nacionalidades com Jogadores Acima de X Overall")

overall_limit = st.sidebar.slider("Defina o Overall Mínimo para o Ranking", min_value=70, max_value=95, value=85)

top_players = df[df['Overall'] >= overall_limit]
top_countries = top_players['Nationality'].value_counts().reset_index().head(5)
top_countries.columns = ['Nationality', 'Number of Players']

st.dataframe(top_countries, use_container_width=True)

st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Análise de Dados com FIFA (2017-2023)")
