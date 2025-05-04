import streamlit as st
from load_data import carregar_todos_os_dados

st.title("💸 Custo-Benefício dos Jogadores (2017-2023)")
df = carregar_todos_os_dados()
df = df.dropna(subset=["value_eur", "overall"])

# Calcula custo-benefício: valor por ponto de overall
df["custo_beneficio"] = df["value_eur"] / df["overall"]

st.markdown("### 🚀 Melhores Custo-Benefício")
st.dataframe(df.sort_values("custo_beneficio").head(10)[["name", "club", "overall", "value_eur", "custo_beneficio", "year"]])

st.markdown("### 💩 Piores Custo-Benefício")
st.dataframe(df.sort_values("custo_beneficio", ascending=False).head(10)[["name", "club", "overall", "value_eur", "custo_beneficio", "year"]])
