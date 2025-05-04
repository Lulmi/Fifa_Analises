import streamlit as st
import pandas as pd
import os
import sys

# ---------------------------- AJUSTE DE CAMINHO PARA IMPORTAÇÃO ---------------------------- #
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from load_data import carregar_todos_os_dados

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="Custo-Benefício dos Jogadores - FIFA",
    page_icon="💸",
    layout="wide"
)

# ---------------------------- CARREGAMENTO DE DADOS ---------------------------- #
df = carregar_todos_os_dados()
df = df.dropna(subset=["value_eur", "overall"])
df = df[df["overall"] > 0]

# ---------------------------- CÁLCULO DO CUSTO-BENEFÍCIO ---------------------------- #
df["custo_beneficio"] = df["value_eur"] / df["overall"]

# ---------------------------- TÍTULO ---------------------------- #
st.title("💸 Custo-Benefício dos Jogadores (2017-2023)")
st.markdown("Análise do custo por ponto de overall: quanto mais baixo, melhor o custo-benefício.")
st.markdown("---")

# ---------------------------- MELHORES CUSTO-BENEFÍCIO ---------------------------- #
st.subheader("🚀 Melhores Custo-Benefício (Menor Custo por Overall)")
melhores = df.sort_values("custo_beneficio").head(10)
st.dataframe(
    melhores[["name", "club", "overall", "value_eur", "custo_beneficio", "year"]],
    use_container_width=True
)

# ---------------------------- PIORES CUSTO-BENEFÍCIO ---------------------------- #
st.subheader("💩 Piores Custo-Benefício (Maior Custo por Overall)")
piores = df.sort_values("custo_beneficio", ascending=False).head(10)
st.dataframe(
    piores[["name", "club", "overall", "value_eur", "custo_beneficio", "year"]],
    use_container_width=True
)

# ---------------------------- FOOTER ---------------------------- #
st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Análise de Custo-Benefício - FIFA (2017-2023)")
