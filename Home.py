import streamlit as st

st.set_page_config(page_title="FIFA Dashboard", layout="wide")

st.title("⚽ Análise Evolutiva dos Jogadores FIFA (2017 - 2023)")

st.markdown("""
Este aplicativo interativo permite explorar a evolução dos jogadores e clubes no FIFA entre 2017 e 2023. 

### 🏠 Páginas disponíveis:
- **Análise de Jogadores**: Filtrar e comparar jogadores por ano, posição, overall e potencial.
- **Análise de Times**: Explorar clubes com maiores médias, número de jogadores e mais.
- **Análises Avançadas**: Tendências de média, idades, nacionalidades e muito mais.

Desenvolvido por Lucas Martins de Oliveira. Dados extraídos do FIFA oficial (2017 a 2023).
""")