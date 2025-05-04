import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="Projeção de Crescimento vs Potential - FIFA",
    page_icon="📊",
    layout="wide"
)

# ---------------------------- FUNÇÃO PARA CARREGAR TODOS OS ANOS ---------------------------- #
@st.cache_data
def load_all_years(data_dir, years):
    data = []
    for y in years:
        df = pd.read_csv(os.path.join(data_dir, f"CLEAN_FIFA{y}_official_data.csv"))
        df['Year'] = int(f"20{y}") if y != "17" else 2017
        data.append(df)
    return pd.concat(data)

# ---------------------------- PARÂMETROS ---------------------------- #
DATA_DIR = "C:/Users/lucas/OneDrive/Documents/Educação/Asimov_Academy/Criando Aplicativos Web com Streamlit/Projeto Streamlit FIFA/datasets/"
years = ["17", "18", "19", "20", "22", "23"]
df_all = load_all_years(DATA_DIR, years)

# ---------------------------- HEADER ---------------------------- #
st.title("📊 Projeção de Crescimento vs Potential (2017-2023)")
st.markdown("Análise de evolução real dos jogadores comparada ao seu potencial previsto no primeiro ano registrado.")
st.markdown("---")

# ---------------------------- FILTRO DE JOGADORES ---------------------------- #
st.sidebar.header("🎯 Filtros")
all_players = sorted(df_all['Name'].unique())
selected_players = st.sidebar.multiselect("Selecione jogadores para ver evolução individual", all_players)

# ---------------------------- EVOLUÇÃO INDIVIDUAL ---------------------------- #
if selected_players:
    evolution_df = df_all[df_all['Name'].isin(selected_players)][['Name', 'Overall', 'Potential', 'Year']]

    st.subheader("📈 Evolução de Overall vs Potential")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=evolution_df, x='Year', y='Overall', hue='Name', marker='o', ax=ax)
    sns.lineplot(data=evolution_df, x='Year', y='Potential', hue='Name', marker='o', ax=ax, linestyle='--', legend=False)
    ax.set_title('Evolução Real (linha sólida) vs Potential (linha pontilhada)')
    st.pyplot(fig)
else:
    st.info("👈 Selecione jogadores na barra lateral para visualizar a evolução.")

# ---------------------------- CLASSIFICAÇÃO DE CRESCIMENTO ---------------------------- #
summary_list = []
for name in df_all['Name'].unique():
    player_data = df_all[df_all['Name'] == name].sort_values('Year')
    if not player_data.empty:
        potential_initial = player_data.iloc[0]['Potential']
        overall_max = player_data['Overall'].max()
        diff = overall_max - potential_initial
        summary_list.append({
            'Name': name,
            'Potential Inicial': potential_initial,
            'Overall Máximo': overall_max,
            'Diferença': diff
        })

summary_df = pd.DataFrame(summary_list)

# ---------------------------- TABELAS DE CATEGORIAS ---------------------------- #
st.subheader("🚀 Jogadores que Superaram o Potencial")
surpassed = summary_df[summary_df['Diferença'] > 0].sort_values(by='Diferença', ascending=False).head(15)
st.dataframe(surpassed, use_container_width=True)

st.subheader("⚖️ Jogadores que Atingiram Parcialmente o Potencial")
partial = summary_df[(summary_df['Diferença'] <= 0) & (summary_df['Diferença'] > -5)].sort_values(by='Diferença', ascending=False).head(15)
st.dataframe(partial, use_container_width=True)

st.subheader("⚠️ Jogadores que Ficaram Abaixo do Potencial")
underachieved = summary_df[summary_df['Diferença'] <= -5].sort_values(by='Diferença').head(15)
st.dataframe(underachieved, use_container_width=True)

st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Crescimento vs Potential - FIFA (2017-2023)")
