import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# ---------------------------- AJUSTE DE CAMINHO PARA IMPORTAÇÃO ---------------------------- #
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from load_data import carregar_todos_os_dados

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="Projeção de Crescimento vs Potential - FIFA",
    page_icon="📊",
    layout="wide"
)

# ---------------------------- CARREGAMENTO DE DADOS ---------------------------- #
df_all = carregar_todos_os_dados()

# ---------------------------- TÍTULO E DESCRIÇÃO ---------------------------- #
st.title("📊 Projeção de Crescimento vs Potential (2017-2023)")
st.markdown("Análise da evolução real dos jogadores comparada ao seu potencial inicial.")
st.markdown("---")

# ---------------------------- FILTRO DE JOGADORES ---------------------------- #
st.sidebar.header("🎯 Filtros")
all_players = sorted(df_all['name'].unique())
selected_players = st.sidebar.multiselect("Selecione jogadores para visualizar evolução", all_players)

# ---------------------------- EVOLUÇÃO INDIVIDUAL ---------------------------- #
if selected_players:
    evolution_df = df_all[df_all['name'].isin(selected_players)][['name', 'overall', 'potential', 'year']]
    st.subheader("📈 Evolução de Overall vs Potential")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=evolution_df, x='year', y='overall', hue='name', marker='o', ax=ax)
    sns.lineplot(data=evolution_df, x='year', y='potential', hue='name', marker='o', ax=ax, linestyle='--', legend=False)
    ax.set_title('Evolução Real (linha sólida) vs Potencial (linha pontilhada)')
    st.pyplot(fig)
else:
    st.info("👈 Selecione jogadores na barra lateral para visualizar a evolução.")

# ---------------------------- CLASSIFICAÇÃO DE CRESCIMENTO ---------------------------- #
summary_list = []
for name in df_all['name'].unique():
    player_data = df_all[df_all['name'] == name].sort_values('year')
    if not player_data.empty:
        potential_initial = player_data.iloc[0]['potential']
        overall_max = player_data['overall'].max()
        diff = overall_max - potential_initial
        summary_list.append({
            'name': name,
            'potential_inicial': potential_initial,
            'overall_maximo': overall_max,
            'diferenca': diff
        })

summary_df = pd.DataFrame(summary_list)

# ---------------------------- TABELAS DE CATEGORIAS ---------------------------- #
st.subheader("🚀 Jogadores que Superaram o Potencial")
surpassed = summary_df[summary_df['diferenca'] > 0].sort_values(by='diferenca', ascending=False).head(15)
st.dataframe(surpassed, use_container_width=True)

st.subheader("⚖️ Jogadores que Atingiram Parcialmente o Potencial")
partial = summary_df[(summary_df['diferenca'] <= 0) & (summary_df['diferenca'] > -5)].sort_values(by='diferenca', ascending=False).head(15)
st.dataframe(partial, use_container_width=True)

st.subheader("⚠️ Jogadores que Ficaram Abaixo do Potencial")
underachieved = summary_df[summary_df['diferenca'] <= -5].sort_values(by='diferenca').head(15)
st.dataframe(underachieved, use_container_width=True)

# ---------------------------- FOOTER ---------------------------- #
st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Crescimento vs Potential - FIFA (2017-2023)")
