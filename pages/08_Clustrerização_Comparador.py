import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ---------------------------- AJUSTE DE CAMINHO ---------------------------- #
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from load_data import carregar_dados

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="Previsão de Overall - FIFA",
    page_icon="📈",
    layout="wide"
)

# ---------------------------- SIDEBAR ---------------------------- #
st.sidebar.header("⚙️ Configurações")
anos_disponiveis = list(range(2017, 2024))
ano = st.sidebar.selectbox("Ano do Dataset", anos_disponiveis)
rodar_modelo = st.sidebar.button("🔍 Treinar Modelo")

# ---------------------------- HEADER ---------------------------- #
st.title("📈 Previsão de Overall dos Jogadores")
st.markdown("Esta página utiliza regressão para prever a **nota geral (Overall)** dos jogadores com base em atributos objetivos.")
st.markdown("---")

# ---------------------------- CARREGAMENTO DOS DADOS ---------------------------- #
df = carregar_dados(ano)

# ---------------------------- FEATURES DISPONÍVEIS ---------------------------- #
feature_cols = ['age', 'potential']
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

target_col = 'overall'

# ---------------------------- VERIFICAÇÃO DE COLUNAS ---------------------------- #
missing = [col for col in feature_cols + [target_col] if col not in df.columns]
if missing:
    st.warning(f"⚠️ As seguintes colunas estão ausentes no dataset de {ano}: {missing}")
    st.stop()

# ---------------------------- PREPARAÇÃO DO MODELO ---------------------------- #
df_model = df.dropna(subset=feature_cols + [target_col]).copy()

st.write(f"📊 Registros disponíveis: `{len(df_model)}`")
if df_model.empty:
    st.error("❌ Nenhum registro disponível após a limpeza. Verifique os dados.")
    st.stop()

X = df_model[feature_cols]
y = df_model[target_col]

# ---------------------------- EXECUÇÃO DO MODELO ---------------------------- #
if rodar_modelo:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # ---------------------------- AVALIAÇÃO ---------------------------- #
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    st.subheader("📊 Avaliação do Modelo")
    st.write(f"**MAE**: {mae:.2f}")
    st.write(f"**RMSE**: {rmse:.2f}")
    st.write(f"**R² Score**: {r2:.2f}")

    with st.expander("ℹ️ O que significam essas métricas?"):
        st.markdown("""
        - **MAE**: Erro médio absoluto entre overall real e previsto  
        - **RMSE**: Penaliza erros grandes  
        - **R²**: Mede a capacidade do modelo em explicar o overall real  
        """)

    # ---------------------------- PLOT REAL VS PREVISTO ---------------------------- #
    st.subheader("🎯 Real vs Previsto")
    fig, ax = plt.subplots()
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.6, ax=ax)
    ax.set_xlabel("Overall Real")
    ax.set_ylabel("Overall Previsto")
    ax.set_title("Dispersão: Overall Real vs Previsto")
    st.pyplot(fig)

    # ---------------------------- IMPORTÂNCIA DAS VARIÁVEIS ---------------------------- #
    st.subheader("📌 Importância das Variáveis")
    importances = pd.Series(model.feature_importances_, index=feature_cols).sort_values()
    fig2, ax2 = plt.subplots()
    importances.plot(kind="barh", ax=ax2)
    ax2.set_title("Importância das Features na Previsão de Overall")
    st.pyplot(fig2)

    # ---------------------------- MAIORES ERROS ---------------------------- #
    st.subheader("⚠️ Maiores Erros")
    df_result = X_test.copy()
    df_result["Overall Real"] = y_test
    df_result["Overall Previsto"] = y_pred
    df_result["Erro Absoluto"] = abs(y_test - y_pred)
    st.dataframe(df_result.sort_values(by="Erro Absoluto", ascending=False).head(10), use_container_width=True)

st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Previsão de Overall - FIFA")
