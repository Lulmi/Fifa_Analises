import streamlit as st
from load_data import carregar_dados

st.title("🏟️ Análise de Times por Ano")
ano = st.selectbox("Selecione o ano:", list(range(2017, 2024)))
df = carregar_dados(ano)

st.markdown("### Clubes com Maior Média de Overall")
st.bar_chart(df.groupby("club")["overall"].mean().sort_values(ascending=False).head(10))

st.markdown("### Clubes com Mais Jogadores na Base")
st.bar_chart(df['club'].value_counts().head(10))

st.markdown("### Detalhamento de Clube")
clube = st.selectbox("Escolha um clube:", sorted(df['club'].dropna().unique()))
df_clube = df[df['club'] == clube]
st.dataframe(df_clube[['name', 'position', 'overall', 'potential']].sort_values("overall", ascending=False).head(15))
