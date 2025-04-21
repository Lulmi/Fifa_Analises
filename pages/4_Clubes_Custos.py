import streamlit as st
from load_data import carregar_todos_os_dados

st.title("🌟 Clubes por Valor de Mercado (2017-2023)")
df = carregar_todos_os_dados()
df = df.dropna(subset=["value_eur", "club"])

# Valor total por clube considerando todos os anos
df_valores = df.groupby("club")["value_eur"].sum().sort_values(ascending=False)

st.markdown("### 💰 Clubes Mais Caros")
st.dataframe(df_valores.head(10))

st.markdown("### 📆 Clubes Mais Baratos")
st.dataframe(df_valores.tail(10))

st.markdown("### 🤔 Clube Budget (valor intermediário)")
if not df_valores.empty:
    budget = df_valores.median()
    st.write(f"Valor intermediário (mediana): €{budget:,.0f}")
    diferencas = df_valores.sub(budget).abs()
    if not diferencas.empty:
        budget_clube = diferencas.idxmin()
        st.write(f"Clube mais próximo da mediana: {budget_clube}")
    else:
        st.warning("Não foi possível calcular o clube mais próximo da mediana.")
else:
    st.warning("Não há dados suficientes para calcular o clube budget.")
