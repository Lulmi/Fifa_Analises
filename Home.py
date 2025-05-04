import streamlit as st

# ---------------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------- #
st.set_page_config(
    page_title="FIFA Players Analysis (2017-2023)",
    page_icon="⚽",
    layout="wide"
)

# ---------------------------- SELETOR DE IDIOMA ---------------------------- #
language = st.sidebar.selectbox("🌐 Escolha o idioma / Choose the language", ["Português", "English"])

# ---------------------------- CONTEÚDO EM PORTUGUÊS ---------------------------- #
if language == "Português":
    st.sidebar.title("Filtros e Navegação")
    st.sidebar.markdown("Use os filtros acima para navegar entre as análises.")

    st.title("⚽ Análise de Jogadores e Times - FIFA (2017-2023)")

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

    ---

    ## 📚 Metodologia e Etapas da Análise

    Este projeto foi dividido em 10 módulos principais:

    1. **Análise de Times** – Médias de atributos por clube, número de jogadores, e relação *Release Clause x Overall*.
    2. **Análise de Jogadores** – Rankings de jogadores, distribuição por país e gráficos de dispersão com Potential.
    3. **Dream Team** – Seleção automática de equipes com base em critérios de overall, custo-benefício e orçamento.
    4. **Evolução dos Jogadores** – Comparação entre potencial inicial e desempenho real ao longo do tempo.
    5. **Análise por Nacionalidade** – Mapas interativos e rankings de países com mais destaque nos dados.
    6. **Time Perfeito e Imperfeito** – Melhor e pior jogador por posição com base no overall.
    7. **Custo-Benefício** – Avaliação do investimento em jogadores baseado em sua performance relativa ao valor de mercado.
    8. **Clusters e Comparador** – Agrupamento de jogadores por perfil técnico e comparação em gráfico radar.
    9. **Previsão de Overall** – Regressão com Random Forest para prever Overall com base em atributos técnicos.
    10. **Previsão de Preço** – Previsão do valor de mercado dos jogadores usando atributos técnicos e físicos.

    Todas as análises contam com visualizações interativas e possibilidade de filtragem por ano, posição, clube, idade e mais.
    """)

# ---------------------------- CONTEÚDO EM INGLÊS ---------------------------- #
else:
    st.sidebar.title("Filters and Navigation")
    st.sidebar.markdown("Use the filters above to navigate through the analyses.")

    st.title("⚽ Player and Team Analysis - FIFA (2017-2023)")

    st.markdown("""
    ## 📊 About this Project

    Welcome to this data analysis portfolio focused on players and teams from the **FIFA** video game series, covering the years **2017 to 2023**.

    The main goal of this project is to explore, visualize, and understand patterns in player attributes, nationalities, positions, teams, and other important factors that influence performance in the game. It also aims to deliver clear insights for both fans of the franchise and data analysts or sports enthusiasts.

    ### 🎯 What you'll find in this project:

    - **Player profile analysis**  
      Comparison of attributes like age, overall rating, potential, position, nationality, and other performance-related factors.

    - **Team profile analysis**  
      Exploration of average attributes across clubs and leagues to identify strengths and weaknesses.

    - **Interactive sidebar filters**  
      You can segment the data by year, club, position, country, age group, and more to personalize your experience.

    - **Rich visual elements**  
      Whenever possible, the analysis includes:
      - **Country flags** 🇧🇷🇦🇷🇫🇷  
      - **Player photos** 🧑‍💼⚽  
      These elements help make the insights more intuitive, informative, and visually pleasant.

    ---

    ## 📂 Data Sources

    This project uses datasets provided by **Kevwe Sophia** on Kaggle, available at:

    **[FIFA23 Official Dataset (Clean Data) - Kaggle](https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data)**

    The datasets were collected for the years **2017 to 2023**, and have already been cleaned for easier analysis.

    ---

    ## 🚀 Next Steps:

    👉 Use the sidebar to navigate between pages:
    - **Home** (this page)
    - **Player Profile Analysis**
    - **Team Profile Analysis**
    - (New pages may be added in the future)

    ---

    ## 📚 Methodology and Analysis Steps

    This project was structured into 10 core modules:

    1. **Team Analysis** – Attribute averages per club, player counts, and *Release Clause vs Overall* visualization.
    2. **Player Analysis** – Player rankings, nationality breakdown, and potential-overall scatterplots.
    3. **Dream Team** – Auto-selection of squads based on best overall, cost-benefit, or budget.
    4. **Player Growth** – Tracking whether players reached, surpassed or underperformed their initial potential.
    5. **Nationality Analysis** – Interactive maps and rankings based on country metrics.
    6. **Perfect and Imperfect XI** – Best and worst players per position by overall rating.
    7. **Cost-Benefit** – Assessment of player efficiency in terms of overall vs market value.
    8. **Clusters & Comparator** – Player clustering by technical profile and radar-based visual comparison.
    9. **Overall Prediction (ML)** – Predicting Overall via Random Forest regression based on technical features.
    10. **Market Value Prediction (ML)** – Predicting market value using a regression model with physical and technical features.

    All pages include dynamic visualizations and filters by year, club, position, age and more.
    """)
