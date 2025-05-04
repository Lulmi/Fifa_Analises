import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# ---------------------------- AJUSTE DE CAMINHO PARA IMPORTAÇÃO ---------------------------- #
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from load_data import carregar_dados

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="Análise por Nacionalidade - FIFA (2017-2023)",
    page_icon="🗺️",
    layout="wide"
)

# ---------------------------- SIDEBAR: ANO ---------------------------- #
st.sidebar.title("⚙️ Filtros")
available_years = ["17", "18", "19", "20", "22", "23"]
year = st.sidebar.selectbox("Selecione o Ano", available_years)
ano_completo = int("20" + year) if year != "17" else 2017

# ---------------------------- CARREGAMENTO DE DADOS ---------------------------- #
df = carregar_dados(ano_completo)

# ---------------------------- HEADER ---------------------------- #
st.title("🗺️ Análise por Nacionalidade - FIFA (2017-2023)")
st.markdown(f"### 📁 Dataset Carregado: `CLEAN_FIFA{year}_official_data.csv`")
st.markdown("---")

# ---------------------------- MAPA: QUANTIDADE DE JOGADORES ---------------------------- #
st.subheader("🌍 Distribuição de Jogadores por Nacionalidade (Mapa Interativo)")
country_counts = df['nationality'].value_counts().reset_index()
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

# ---------------------------- MAPA: MÉDIA DE OVERALL POR PAÍS ---------------------------- #
st.subheader("🌍 Média de Overall por Nacionalidade (Mapa Interativo)")
overall_avg = df.groupby('nationality')['overall'].mean().reset_index()
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

# ---------------------------- GRÁFICO DE BARRAS ---------------------------- #
st.subheader("📊 Média de Overall e Potential por Nacionalidade (Top 15 Países com mais jogadores)")
overall_potential_avg = df.groupby('nationality')[['overall', 'potential']].mean().reset_index()
top_15 = df['nationality'].value_counts().head(15).index
overall_potential_avg = overall_potential_avg[overall_potential_avg['nationality'].isin(top_15)]

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    data=overall_potential_avg.melt(id_vars='nationality', value_vars=['overall', 'potential']),
    x='nationality',
    y='value',
    hue='variable',
    ax=ax
)
plt.title('Média de Overall e Potential por Nacionalidade (Top 15)')
plt.ylabel('Média')
plt.xlabel('Nacionalidade')
plt.xticks(rotation=45)
st.pyplot(fig)

# ---------------------------- TOP NACIONALIDADES POR OVERALL ---------------------------- #
st.subheader("🏆 Top 5 Nacionalidades com Jogadores Acima de X Overall")
overall_limit = st.sidebar.slider("Defina o Overall Mínimo", min_value=70, max_value=95, value=85)
top_players = df[df['overall'] >= overall_limit]
top_countries = top_players['nationality'].value_counts().reset_index().head(5)
top_countries.columns = ['Nationality', 'Number of Players']
st.dataframe(top_countries, use_container_width=True)

# ---------------------------- FOOTER ---------------------------- #
st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Análise por Nacionalidade - FIFA (2017-2023)")
