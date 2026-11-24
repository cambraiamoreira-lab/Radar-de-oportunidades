
import streamlit as st

from catalogo_apis import (
    listar_apis,
    listar_segmentos,
    resumo_catalogo
)

st.set_page_config(
    page_title="Radar de Oportunidades",
    page_icon="📡",
    layout="wide"
)

st.title("📡 RADAR DE OPORTUNIDADES")

st.caption(
    "Descoberta de APIs brasileiras e oportunidades digitais"
)

st.divider()

# INDICADORES

resumo = resumo_catalogo()

col1, col2, col3 = st.columns(3)

col1.metric(
    "APIs cadastradas",
    resumo["total_apis"]
)

col2.metric(
    "Segmentos identificados",
    resumo["segmentos"]
)

col3.metric(
    "Consultas testadas",
    resumo["consultas_testadas"]
)

st.divider()

# FILTRO

st.header("🔎 Catálogo brasileiro de APIs")

segmentos = ["Todos"] + listar_segmentos()

segmento_escolhido = st.selectbox(
    "Filtrar por segmento",
    segmentos
)

apis = listar_apis()

if segmento_escolhido != "Todos":

    apis = [
        api for api in apis
        if api["segmento"] == segmento_escolhido
    ]

st.write(
    f"**{len(apis)} APIs encontradas no catálogo**"
)

# LISTAGEM

for api in apis:

    with st.expander(
        f"🌐 {api['nome']} | {api['segmento']}"
    ):

        st.write("**Órgão responsável:**", api["orgao"])

        st.write("**Origem:**", api["origem"])

        st.write("**Descrição:**", api["descricao"])

        st.write("**Dados disponíveis:**")

        for dado in api["dados_disponiveis"]:
            st.write(f"• {dado}")

        st.write("**Possíveis aplicações:**")

        for aplicacao in api["aplicacoes_hipoteticas"]:
            st.write(f"• {aplicacao}")

        st.divider()

        st.write(
            "**Modelo de acesso:**",
            api["modelo_acesso"]
        )

        st.write(
            "**Necessidade de chave:**",
            api["exige_chave"]
        )

        st.write(
            "**Gratuidade:**",
            api["gratuidade"]
        )

        st.write(
            "**Uso comercial:**",
            api["uso_comercial"]
        )

        st.write(
            "**Situação:**",
            api["status"]
        )

        st.link_button(
            "Consultar documentação",
            api["documentacao"]
        )

        st.link_button(
            "Acessar fonte",
            api["url_acesso"]
        )

st.divider()

st.header("🧭 Próximas análises")

st.info(
    "As APIs estão cadastradas. A próxima etapa será "
    "verificar tecnicamente o acesso, a autenticação, "
    "os limites, a atualização dos dados e as condições "
    "de uso comercial."
)

st.caption(
    "RADAR DE OPORTUNIDADES | Nova arquitetura | Versão 1.0"
)
