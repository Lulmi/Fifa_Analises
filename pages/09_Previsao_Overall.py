import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="Previsão de Overall - FIFA",
    page_icon="📈",
    layout="wide"
)

# ---------------------------- FUNÇÕES AUXILIARES ---------------------------- #
@st.cache_data
def load_data(data_dir, year):
    file_path = os.path.join(data_dir, f"CLEAN_FIFA{year}_official_data.csv")
    df = pd.read_csv(file_path)
    df['Year'] = int(f"20{year}") if year != "17" else 2017
    return df

@st.cache_data
def get_feature_data(df, target_col, features):
    df_model = df.dropna(subset=features + [target_col]).copy()
    X = df_model[features]
    y = df_model[target_col]
    return train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------------------- SIDEBAR ---------------------------- #
st.sidebar.header("⚙️ Configurações")
DATA_DIR = "C:/Users/lucas/OneDrive/Documents/Educação/Asimov_Academy/Criando Aplicativos Web com Streamlit/Projeto Streamlit FIFA/datasets/"
years = ["17", "18", "19", "20", "22", "23"]
selected_year = st.sidebar.selectbox("Ano do Dataset", years)
run_model = st.sidebar.button("🔍 Treinar Modelo")

# ---------------------------- HEADER ---------------------------- #
st.title("📈 Previsão de Overall dos Jogadores")
st.markdown("Esta análise utiliza algoritmos de regressão para prever o atributo 'Overall' dos jogadores com base em seus atributos técnicos e físicos.")
st.markdown("---")

# ---------------------------- FEATURE SELECTION ---------------------------- #
feature_cols = [
    'Acceleration', 'SprintSpeed', 'Agility', 'Balance', 'Strength',
    'BallControl', 'Dribbling', 'ShortPassing', 'LongPassing',
    'Finishing', 'ShotPower', 'Marking', 'StandingTackle', 'SlidingTackle'
]
target_col = 'Overall'

# ---------------------------- CARREGAMENTO DOS DADOS ---------------------------- #
df = load_data(DATA_DIR, selected_year)

if run_model:
    X_train, X_test, y_train, y_test = get_feature_data(df, target_col, feature_cols)

    model = RandomForestRegressor(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    st.subheader("📊 Avaliação do Modelo")
    st.write(f"**MAE**: {mae:.2f}")
    st.write(f"**RMSE**: {rmse:.2f}")
    st.write(f"**R² Score**: {r2:.2f}")

    with st.expander("ℹ️ O que significam essas métricas?"):
        st.markdown("""
        ### 🔹 MAE – Erro Absoluto Médio
        Mostra o erro médio das previsões. Quanto menor, melhor. Ex: MAE = 1.8 indica erro médio de 1.8 pontos no Overall.

        ### 🔹 RMSE – Raiz do Erro Quadrático Médio
        Parecido com o MAE, mas penaliza mais os erros grandes. Ideal se estiver próximo ao MAE e for baixo.

        ### 🔹 R² Score – Coeficiente de Determinação
        Mede a qualidade geral do modelo. Varia de 0 a 1. Ex: R² = 0.85 significa que o modelo explica 85% do comportamento real dos dados.
        """)

    # ---------------------------- GRÁFICO REAL VS PREVISTO ---------------------------- #
    st.subheader("🎯 Real vs Previsto")
    fig, ax = plt.subplots()
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.6, ax=ax)
    ax.set_xlabel("Overall Real")
    ax.set_ylabel("Overall Previsto")
    ax.set_title("Dispersão: Real vs Previsto")
    st.pyplot(fig)

    # ---------------------------- FEATURE IMPORTANCE ---------------------------- #
    st.subheader("📌 Importância das Variáveis")
    importances = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=True)
    fig2, ax2 = plt.subplots()
    importances.plot(kind='barh', ax=ax2)
    ax2.set_title("Importância das Features na Previsão do Overall")
    st.pyplot(fig2)

    # ---------------------------- MAIORES ERROS ---------------------------- #
    st.subheader("⚠️ Maiores Erros na Previsão")
    df_results = X_test.copy()
    df_results['Overall Real'] = y_test
    df_results['Overall Previsto'] = y_pred
    df_results['Erro Absoluto'] = abs(y_test - y_pred)
    st.dataframe(df_results.sort_values(by='Erro Absoluto', ascending=False).head(10), use_container_width=True)

st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Previsão de Atributos - FIFA (2017-2023)")
