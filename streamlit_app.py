
import streamlit as st

st.set_page_config(
    page_title="Radar de Oportunidades",
    page_icon="📡",
    layout="wide"
)

# Identidade visual
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0;
    }
    .subtitle {
        color: #8b949e;
        font-size: 1rem;
        margin-top: 5px;
    }
    .panel {
        padding: 20px;
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 12px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown(
    '<div class="main-title">📡 RADAR DE OPORTUNIDADES</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Inteligência para descobrir, avaliar e transformar dados em oportunidades.</div>',
    unsafe_allow_html=True
)

st.divider()

# Situação do projeto
st.subheader("Central de inteligência")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Fontes cadastradas", "0")

with col2:
    st.metric("Oportunidades identificadas", "0")

with col3:
    st.metric("Análises realizadas", "0")

st.divider()

# Apresentação
st.subheader("🔎 O que estamos procurando?")

st.markdown("""
O Radar investiga fontes de dados e serviços digitais para encontrar
possibilidades de criação de ferramentas úteis e comercializáveis.
""")

# Critérios de avaliação
st.subheader("📊 Critérios de avaliação")

criterios = [
    ("Acessibilidade", "É possível acessar os dados na prática?"),
    ("Custo", "O acesso é gratuito, limitado ou pago?"),
    ("Confiabilidade", "Os dados são confiáveis e atualizados?"),
    ("Utilidade", "Que problemas podem ser resolvidos?"),
    ("Potencial comercial", "Existe possibilidade de monetização?")
]

for titulo, descricao in criterios:
    with st.container(border=True):
        st.markdown(f"**{titulo}**")
        st.caption(descricao)

st.divider()

# Fontes de pesquisa
st.subheader("🌐 Fontes de pesquisa")

st.info(
    "O mecanismo de pesquisa ainda está em desenvolvimento. "
    "Nenhuma fonte foi validada nesta versão inicial."
)

st.markdown("""
**Fontes previstas para investigação:**

- APIs públicas e documentadas
- Portais oficiais de dados abertos
- Bases econômicas e financeiras
- Informações de clima e transporte
- Outras fontes verificáveis
""")

st.divider()

st.caption(
    "RADAR DE OPORTUNIDADES | Versão inicial 0.1"
)

