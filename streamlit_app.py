
import streamlit as st
from fontes_mercado import (
    listar_fontes,
    contar_fontes,
    fontes_publicas
)

st.set_page_config(
    page_title="Radar de Oportunidades",
    page_icon="📡",
    layout="wide"
)

st.title("📡 RADAR DE OPORTUNIDADES")
st.caption("Inteligência para descobrir negócios digitais no Brasil.")

st.divider()

fontes = listar_fontes()
publicas = fontes_publicas()

col1, col2, col3 = st.columns(3)

col1.metric("Fontes cadastradas", contar_fontes())
col2.metric("Fontes de consulta pública", len(publicas))
col3.metric("Oportunidades validadas", 0)

st.divider()

st.header("🔎 Central de investigação")

st.write(
    "O Radar investiga problemas reais, demandas de mercado "
    "e oportunidades para criação de ferramentas digitais."
)

st.header("🌐 Fontes de inteligência")

for fonte in fontes:
    with st.expander(f"{fonte['nome']} | {fonte['categoria']}"):
        st.write("**Público:**", fonte["publico"])
        st.write("**Descrição:**", fonte["descricao"])
        st.write("**Acesso:**", fonte["acesso"])
        st.write("**Potencial:**", fonte["potencial"])
        st.write("**Situação:**", fonte["status"])
        st.link_button("Consultar fonte", fonte["url"])

st.divider()

st.header("📊 Critérios de avaliação")

criterios = [
    "Demanda de mercado",
    "Concorrência",
    "Potencial de receita",
    "Disponibilidade de dados",
    "Custo de desenvolvimento",
    "Facilidade de lançamento"
]

for criterio in criterios:
    st.write("•", criterio)

st.info(
    "O Radar está em fase de construção. "
    "As fontes cadastradas ainda precisam passar por validação "
    "e análise de seus dados."
)

st.caption("RADAR DE OPORTUNIDADES | Versão 0.2")
