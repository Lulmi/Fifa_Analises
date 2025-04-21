import streamlit as st
from load_data import carregar_todos_os_dados

st.title("🏆 Probabilidade de Vitória/Derrota por Clube (2017-2023)")
df = carregar_todos_os_dados()
df = df.dropna(subset=["club", "overall"])

df_clubes = df.groupby("club")["overall"].mean().sort_values(ascending=False)

st.markdown("### 🚀 Clubes com Maior Chance de Vitória")
st.dataframe(df_clubes.head(10))

st.markdown("### 💩 Clubes com Maior Risco de Derrota")
st.dataframe(df_clubes.tail(10))