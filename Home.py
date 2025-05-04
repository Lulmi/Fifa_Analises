import streamlit as st

# Configurações iniciais da página
st.set_page_config(
    page_title="FIFA Players Analysis (2017-2023)",
    page_icon="⚽",
    layout="wide"
)

# Sidebar
st.sidebar.title("Filtros e Navegação")
st.sidebar.markdown("Use os filtros acima para navegar entre as análises.")

# Título principal da página
st.title("⚽ Análise de Jogadores e Times - FIFA (2017-2023)")

# Descrição detalhada
st.markdown("""
## 📊 Sobre este Projeto

Bem-vindo ao portfólio de análise de dados focado em jogadores e times dos jogos da série **FIFA**, cobrindo os anos de **2017 a 2023**.

Este projeto tem como principal objetivo explorar, visualizar e compreender os padrões presentes nos atributos dos jogadores, suas nacionalidades, posições, times e outros fatores importantes que influenciam o desempenho no jogo. Além disso, buscamos fornecer insights de fácil interpretação tanto para quem é fã da franquia quanto para analistas de dados e entusiastas de esportes.

### 🎯 O que você encontrará neste projeto:

- **Análise de perfil de jogadores**  
  Comparação entre atributos como idade, overall (pontuação geral), potencial, posição, nacionalidade e outros fatores que contribuem para o desempenho dos atletas.

- **Análise de perfil de times**  
  Exploração das médias de atributos entre jogadores de diferentes clubes e ligas, visualizando as forças e fraquezas de cada equipe.

- **Filtros interativos na barra lateral**  
  Você poderá segmentar os dados por ano, time, posição, país, faixa etária, entre outros, para uma experiência personalizada de análise.

- **Elementos visuais enriquecidos**  
  Sempre que possível, serão exibidas:
  - **Bandeiras dos países** 🇧🇷🇦🇷🇫🇷  
  - **Fotos dos jogadores** 🧑‍💼⚽  
  Isso torna a análise mais intuitiva, informativa e visualmente agradável.

---

## 📂 Fontes dos Dados

Este projeto utiliza os conjuntos de dados disponibilizados por **Kevwe Sophia** no Kaggle, no seguinte link:

**[FIFA23 Official Dataset (Clean Data) - Kaggle](https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data)**

As bases foram coletadas para os anos de **2017 a 2023**, já devidamente tratadas e limpas para facilitar a análise.

---

## 🚀 Próximos passos:

👉 Use a barra lateral para navegar entre as páginas:
- **Home** (esta página)
- **Análise de Perfil de Jogadores**
- **Análise de Perfil de Times**
- (Novas análises poderão ser adicionadas futuramente)

""")
