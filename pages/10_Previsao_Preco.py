import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="Previsão de Valor de Mercado - FIFA",
    page_icon="💸",
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
st.title("💸 Previsão de Valor de Mercado dos Jogadores")
st.markdown("Utiliza regressão para prever o valor de mercado dos jogadores com base em seus atributos físicos e técnicos.")
st.markdown("---")

# ---------------------------- FEATURE SELECTION ---------------------------- #
feature_cols = [
    'Age', 'Overall', 'Potential', 'Acceleration', 'SprintSpeed', 'Agility',
    'BallControl', 'Dribbling', 'ShortPassing', 'Finishing',
    'ShotPower', 'Strength', 'Composure', 'Positioning'
]
target_col = 'Value(£)'

# ---------------------------- CARREGAMENTO DOS DADOS ---------------------------- #
df = load_data(DATA_DIR, selected_year)

if run_model:
    if target_col not in df.columns:
        st.error(f"❌ A coluna '{target_col}' não está disponível neste ano selecionado.")
    else:
        X_train, X_test, y_train, y_test = get_feature_data(df, target_col, feature_cols)

        model = RandomForestRegressor(random_state=42, n_estimators=100)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        st.subheader("📊 Avaliação do Modelo")
        st.write(f"**MAE**: £{mae:,.0f}")
        st.write(f"**RMSE**: £{rmse:,.0f}")
        st.write(f"**R² Score**: {r2:.2f}")

        with st.expander("ℹ️ O que significam essas métricas?"):
            st.markdown("""
            ### 🔹 MAE – Erro Absoluto Médio
            Mostra o erro médio nas previsões do valor de mercado. Quanto menor, melhor.

            ### 🔹 RMSE – Raiz do Erro Quadrático Médio
            Penaliza mais os erros grandes. Ideal se estiver próximo do MAE.

            ### 🔹 R² Score – Coeficiente de Determinação
            Mede o quanto o modelo explica do valor de mercado real. Vai de 0 (fraco) a 1 (ótimo).
            """)

        # ---------------------------- GRÁFICO REAL VS PREVISTO ---------------------------- #
        st.subheader("🎯 Real vs Previsto")
        fig, ax = plt.subplots()
        sns.scatterplot(x=y_test, y=y_pred, alpha=0.6, ax=ax)
        ax.set_xlabel("Valor Real (£)")
        ax.set_ylabel("Valor Previsto (£)")
        ax.set_title("Dispersão: Valor Real vs Previsto")
        st.pyplot(fig)

        # ---------------------------- FEATURE IMPORTANCE ---------------------------- #
        st.subheader("📌 Importância das Variáveis")
        importances = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=True)
        fig2, ax2 = plt.subplots()
        importances.plot(kind='barh', ax=ax2)
        ax2.set_title("Importância das Features na Previsão do Valor")
        st.pyplot(fig2)

        # ---------------------------- MAIORES ERROS ---------------------------- #
        st.subheader("⚠️ Maiores Erros na Previsão")
        df_results = X_test.copy()
        df_results['Valor Real (£)'] = y_test
        df_results['Valor Previsto (£)'] = y_pred
        df_results['Erro Absoluto (£)'] = abs(y_test - y_pred)
        st.dataframe(df_results.sort_values(by='Erro Absoluto (£)', ascending=False).head(10), use_container_width=True)

st.markdown("---")
st.markdown("🖥️ Projeto desenvolvido por Lucas Martins de Oliveira - Previsão de Atributos - FIFA (2017-2023)")
