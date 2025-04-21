import streamlit as st
from load_data import carregar_todos_os_dados
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📈 Análises Avançadas (2017 a 2023)")
df = carregar_todos_os_dados()

st.markdown("### Evolução da Média de Overall")
media_ano = df.groupby("year")["overall"].mean()
media_ano.index = media_ano.index.astype(str)  # transforma os anos em string
st.line_chart(media_ano)

st.markdown("### Dispersão: Overall vs Potential")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x="overall", y="potential", hue="year", alpha=0.3, ax=ax)
plt.title("Potencial x Overall por Jogador")
st.pyplot(fig)

st.markdown("### Nacionalidades Mais Frequentes")
nac = df['nationality'].value_counts().head(10)
st.bar_chart(nac)

st.markdown("### Correlação entre Idade, Overall e Potential")
corr = df[['age', 'overall', 'potential']].corr()
st.dataframe(corr.round(2))