import streamlit as st
from load_data import carregar_todos_os_dados

st.title("✨ Time Perfeito e Time Imperfeito (2017-2023)")
df = carregar_todos_os_dados()
df = df.dropna(subset=["position", "overall"])

# Time Perfeito: maior overall por posição
st.markdown("### 🌟 Time Perfeito")
df_top = df.sort_values("overall", ascending=False).drop_duplicates("position")
st.dataframe(df_top[['name', 'position', 'overall', 'club', 'year']])

# Time Imperfeito: menor overall por posição
st.markdown("### 💩 Time Imperfeito")
df_bot = df.sort_values("overall").drop_duplicates("position")
st.dataframe(df_bot[['name', 'position', 'overall', 'club', 'year']])