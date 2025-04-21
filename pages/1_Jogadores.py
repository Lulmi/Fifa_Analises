import streamlit as st
from load_data import carregar_dados

st.title("📊 Análise de Jogadores por Ano")
ano = st.selectbox("Selecione o ano desejado:", list(range(2017, 2024)))
df = carregar_dados(ano)

st.markdown("### Top 10 Jogadores por Overall")
st.dataframe(df.sort_values("overall", ascending=False)[['name', 'club', 'age', 'nationality', 'overall', 'potential']].head(10))

st.markdown("### Distribuição de Idade")
st.bar_chart(df['age'].value_counts().sort_index())

st.markdown("### Jogadores por Posição")
pos = st.selectbox("Selecione a posição:", sorted(df['position'].dropna().unique()))
df_pos = df[df['position'] == pos]
st.dataframe(df_pos[['name', 'club', 'overall', 'potential']].sort_values("overall", ascending=False).head(10))