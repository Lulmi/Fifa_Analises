import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# ---------------------------- AJUSTE DE CAMINHO ---------------------------- #
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from load_data import carregar_dados

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="Clusters e Comparador de Jogadores - FIFA",
    page_icon="🧠",
    layout="wide"
)

# ---------------------------- PARÂMETROS ---------------------------- #
st.sidebar.header("🔧 Filtros")
anos_disponiveis = list(range(2017, 2024))
ano = st.sidebar.selectbox("Selecione o Ano", anos_disponiveis)
df = carregar_dados(ano)

# ---------------------------- FILTROS E FEATURES ---------------------------- #
st.title("🧠 Clusterização de Jogadores e Comparador - FIFA")
st.markdown("Agrupamento de jogadores com base em atributos contratuais e desempenho geral.")
st.markdown("---")

# Verifica colunas disponíveis
feature_cols = ['age', 'overall', 'potential']
extra_cols = []
if 'value(£)' in df.columns:
    feature_cols.append('value(£)')
    extra_cols.append('value(£)')
if 'wage(£)' in df.columns:
    feature_cols.append('wage(£)')
    extra_cols.append('wage(£)')
if 'release clause(£)' in df.columns:
    feature_cols.append('release clause(£)')
    extra_cols.append('release clause(£)')

# ---------------------------- CLUSTERIZAÇÃO ---------------------------- #
df_cluster = df.dropna(subset=feature_cols).copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_cluster[feature_cols])

k = st.sidebar.slider("Número de Clusters", min_value=2, max_value=10, value=5)
kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
df_cluster['cluster'] = kmeans.fit_predict(X_scaled)

# ---------------------------- PLOT ---------------------------- #
st.subheader("📊 Visualização dos Clusters (2D PCA Simples)")
df_cluster['AxisX'] = X_scaled[:, 0]
df_cluster['AxisY'] = X_scaled[:, 1]
fig = px.scatter(
    df_cluster, x='AxisX', y='AxisY', color=df_cluster['cluster'].astype(str),
    hover_data=['name', 'age', 'overall', 'potential'] + extra_cols,
    title="Agrupamento de Jogadores (Clusters)",
    color_discrete_sequence=px.colors.qualitative.Set1
)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------- INTERPRETAÇÃO ---------------------------- #
st.subheader("📄 Resumo dos Clusters")
resumo = df_cluster.groupby('cluster').agg({
    'overall': 'mean',
    'potential': 'mean',
    'age': 'mean',
    **{col: 'mean' for col in extra_cols}
}).round(2)
st.dataframe(resumo, use_container_width=True)

# ---------------------------- COMPARADOR ---------------------------- #
st.markdown("---")
st.subheader("📊 Comparador de Jogadores - Radar")
players = st.sidebar.multiselect("Selecione até 5 Jogadores", sorted(df_cluster['name'].unique()))

if players:
    radar_features = ['age', 'overall', 'potential'] + extra_cols
    compare_df = df_cluster[df_cluster['name'].isin(players)][['name'] + radar_features].copy()

    def normalize(col):
        return 100 * (col - col.min()) / (col.max() - col.min())

    for col in radar_features:
        compare_df[col] = normalize(compare_df[col])

    fig_radar = go.Figure()
    for _, row in compare_df.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=row[radar_features].values,
            theta=radar_features,
            fill='toself',
            name=row['name']
        ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title="Radar Comparativo entre Jogadores"
    )
    st.plotly_chart(fig_radar, use_container_width=True)
else:
    st.info("👈 Selecione jogadores na barra lateral para compará-los em formato radar.")

# ---------------------------- FOOTER ---------------------------- #
st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Clusterização e Comparação de Jogadores")
