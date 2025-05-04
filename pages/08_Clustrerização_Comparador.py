import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="Clusters e Comparador de Jogadores - FIFA",
    page_icon="🧠",
    layout="wide"
)

# ---------------------------- FUNÇÕES AUXILIARES ---------------------------- #
@st.cache_data
def load_data(data_dir, years):
    data = []
    for y in years:
        df = pd.read_csv(os.path.join(data_dir, f"CLEAN_FIFA{y}_official_data.csv"))
        df['Year'] = int(f"20{y}") if y != "17" else 2017
        data.append(df)
    return pd.concat(data)

@st.cache_data
def compute_simple_clusters(df, features, n_clusters=6):
    df = df.dropna(subset=features).copy()
    df['Feature_Mean'] = df[features].mean(axis=1)

    if df['Feature_Mean'].nunique() < n_clusters:
        df['Cluster'] = 0
    else:
        df['Cluster'] = pd.qcut(df['Feature_Mean'], q=n_clusters, labels=False, duplicates='drop')

    df['AxisX'] = df['Dribbling']
    df['AxisY'] = df['Finishing']
    return df

# ---------------------------- PARÂMETROS E CARREGAMENTO ---------------------------- #
DATA_DIR = "C:/Users/lucas/OneDrive/Documents/Educação/Asimov_Academy/Criando Aplicativos Web com Streamlit/Projeto Streamlit FIFA/datasets/"
years = ["17", "18", "19", "20", "22", "23"]
df_all = load_data(DATA_DIR, years)

# ---------------------------- CLUSTERIZAÇÃO ---------------------------- #
st.title("🧠 Clusters de Jogadores e Comparador (2017-2023)")
st.markdown("Agrupamento de jogadores por estilo e atributos físicos/técnicos.")
st.markdown("---")

st.sidebar.header("🔧 Filtros")
selected_year = st.sidebar.selectbox("Selecione o Ano para Clusterização", sorted(df_all['Year'].unique(), reverse=True))

# ---------------------------- CLUSTERIZAÇÃO E ANÁLISE ---------------------------- #
df_year = df_all[df_all['Year'] == selected_year].copy()

features = [
    'Acceleration', 'SprintSpeed', 'Agility', 'Balance', 'Strength',
    'BallControl', 'Dribbling', 'ShortPassing', 'LongPassing',
    'Finishing', 'ShotPower', 'Marking', 'StandingTackle', 'SlidingTackle'
]

df_clustered = compute_simple_clusters(df_year, features)

fig = px.scatter(
    df_clustered, x='AxisX', y='AxisY', color=df_clustered['Cluster'].astype(str),
    hover_data=['Name', 'Club', 'Position', 'Overall'],
    title='Agrupamento de Jogadores com Base em Atributos Técnicos',
    labels={'AxisX': 'Dribbling', 'AxisY': 'Finishing'},
    color_discrete_sequence=px.colors.qualitative.Set1
)

st.plotly_chart(fig, use_container_width=True)

# Legenda explicativa dos clusters e tabela dinâmica
st.markdown("### 📄 Interpretação dos Clusters")
cluster_summary = df_clustered.groupby('Cluster').agg({
    'Feature_Mean': 'mean',
    'Overall': 'mean',
    'Age': 'mean'
}).rename(columns={
    'Feature_Mean': 'Média de Atributos',
    'Overall': 'Overall Médio',
    'Age': 'Idade Média'
}).reset_index()
st.dataframe(cluster_summary, use_container_width=True)

# Análises derivadas: promessas, veteranos, craques
st.markdown("### 🔎 Destaques por Perfil")
min_overall_young = st.sidebar.slider("Overall mínimo - Jovens Promessas", 60, 85, 70)
min_overall_old = st.sidebar.slider("Overall mínimo - Veteranos", 60, 90, 70)
min_overall_star = st.sidebar.slider("Overall mínimo - Craques", 80, 95, 87)
max_age_young = st.sidebar.slider("Idade máxima - Jovens Promessas", 18, 25, 21)
min_age_old = st.sidebar.slider("Idade mínima - Veteranos", 30, 40, 33)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🌱 Jovens Promessas")
    df_promessas = df_clustered[(df_clustered['Age'] <= max_age_young) & (df_clustered['Overall'] >= min_overall_young)]
    st.dataframe(df_promessas[['Name', 'Age', 'Overall', 'Potential', 'Club']].sort_values(by='Potential', ascending=False).head(10), use_container_width=True)

with col2:
    st.markdown("#### 🧓 Veteranos em Atividade")
    df_veteranos = df_clustered[(df_clustered['Age'] >= min_age_old) & (df_clustered['Overall'] >= min_overall_old)]
    st.dataframe(df_veteranos[['Name', 'Age', 'Overall', 'Potential', 'Club']].sort_values(by='Overall', ascending=False).head(10), use_container_width=True)

with col3:
    st.markdown("#### 🌟 Craques do Jogo")
    df_craques = df_clustered[df_clustered['Overall'] >= min_overall_star]
    st.dataframe(df_craques[['Name', 'Age', 'Overall', 'Potential', 'Club']].sort_values(by='Overall', ascending=False).head(10), use_container_width=True)

# ---------------------------- COMPARADOR DE JOGADORES ---------------------------- #
st.markdown("---")
st.subheader("📊 Comparador de Jogadores - Gráfico Radar")
players = st.sidebar.multiselect("Selecione até 5 Jogadores para Comparação", options=sorted(df_year['Name'].unique()))

if players:
    compare_df = df_year[df_year['Name'].isin(players)].copy()
    radar_features = ['Acceleration', 'SprintSpeed', 'Agility', 'Dribbling', 'ShortPassing', 'Finishing', 'Strength']

    def normalize(series):
        return 100 * (series - series.min()) / (series.max() - series.min())

    radar_df = compare_df[['Name'] + radar_features].copy()
    for col in radar_features:
        radar_df[col] = normalize(radar_df[col])

    fig_radar = go.Figure()
    for i, row in radar_df.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=row[radar_features].values,
            theta=radar_features,
            fill='toself',
            name=row['Name']
        ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True,
        title="Radar Comparativo dos Atributos Selecionados"
    )

    st.plotly_chart(fig_radar, use_container_width=True)
else:
    st.info("👈 Selecione jogadores na barra lateral para comparar atributos em formato radar.")

st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Clusters e Comparador - FIFA (2017-2023)")
