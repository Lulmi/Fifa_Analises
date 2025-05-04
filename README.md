# ⚽ FIFA Players Analysis (2017–2023)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-ff4b4b)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Language Support](https://img.shields.io/badge/Idioma-Português--Inglês-yellow.svg)](#-idiomas)

📢 **Esta documentação está dividida em duas seções:**  
1️⃣ **Português**  
2️⃣ **English (scroll down ⬇)**

---

## 🇧🇷 DOCUMENTAÇÃO EM PORTUGUÊS

---

## 📚 Sumário

- [🌍 Idiomas](#-idiomas)
- [📦 Tecnologias e Ferramentas](#-tecnologias-e-ferramentas-utilizadas)
- [🧠 Estrutura do Projeto](#-estrutura-do-projeto)
- [🧭 Como Rodar](#-como-rodar-o-projeto)

---

## 🌍 Idiomas

- 🇧🇷 Português  
- 🇺🇸 Inglês  
> Um seletor de idioma permite alternar dinamicamente entre os idiomas na aplicação.

---

## 📦 Tecnologias e Ferramentas Utilizadas

| Categoria             | Ferramenta / Biblioteca            |
|-----------------------|------------------------------------|
| Web App               | Streamlit                          |
| Análise de Dados      | Pandas, NumPy                      |
| Visualização de Dados | Seaborn, Matplotlib, Plotly        |
| Machine Learning      | Scikit-learn (Random Forest)       |
| Organização           | Modularização com múltiplas páginas |
| Dataset Original      | Kaggle - FIFA Official Clean Data  |

---

## 🧠 Estrutura do Projeto

A aplicação contém **10 páginas principais**, cada uma com foco específico:

1️⃣ **Análise de Times**  
> Médias de atributos, jogadores por clube, cláusula de rescisão x overall.

2️⃣ **Análise de Jogadores**  
> Top 10 e Bottom 10, nacionalidades, relação Potential x Overall.

3️⃣ **Dream Team**  
> Montagem automática de time ideal:
- Melhor Overall  
- Melhor Custo-Benefício  
- Melhor time dentro de um orçamento

4️⃣ **Evolução de Jogadores**  
> Comparação entre evolução real e potencial previsto ao longo dos anos.

5️⃣ **Nacionalidades**  
> Mapa interativo com número de jogadores e média de atributos por país.

6️⃣ **Time Perfeito e Imperfeito**  
> Melhor e pior jogador por posição com base no Overall.

7️⃣ **Custo-Benefício**  
> ROI: valor de mercado dividido pelo overall.

8️⃣ **Clusterização e Comparador**  
> Agrupamento por estilo de jogo + gráfico radar comparativo.

9️⃣ **Previsão de Overall**  
> Modelo de ML para prever o Overall com base em atributos.

🔟 **Previsão de Preço**  
> Modelo de regressão para prever valor de mercado.

---

## 🧭 Como Rodar o Projeto

### 🔹 Pré-requisitos

- Python 3.8+
- Instalar dependências:
```bash
pip install -r requirements.txt
