
import streamlit as st

from catalogo_apis import (
    listar_apis,
    listar_segmentos,
    resumo_catalogo
)

from verificador_apis import testar_banco_central


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

# CATÁLOGO

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

# VERIFICADOR DE APIS

st.header("🧪 Laboratório de testes")

st.write(
    "Vamos verificar se uma API brasileira responde "
    "e entrega dados reais."
)

st.subheader("Banco Central do Brasil")

st.write(
    "Teste da série histórica de cotação de compra do dólar."
)

if st.button(
    "🚀 Testar API do Banco Central",
    type="primary"
):

    with st.spinner("Conectando ao Banco Central..."):

        resultado = testar_banco_central()

    if (
        resultado["status"] == "Acessível"
        and resultado["tem_dados"]
    ):

        st.success("API respondeu e retornou dados!")

    elif resultado["status"] == "Acessível":

        st.warning("API respondeu, mas não foram encontrados dados.")

    else:

        st.error("O teste identificou um problema.")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Status",
        resultado["status"]
    )

    col2.metric(
        "Código HTTP",
        resultado["codigo_http"]
        if resultado["codigo_http"] is not None
        else "N/A"
    )

    col3.metric(
        "Tempo de resposta",
        f"{resultado['tempo_resposta']} s"
        if resultado["tempo_resposta"] is not None
        else "N/A"
    )

    st.write(
        "**Formato recebido:**",
        resultado["formato"]
    )

    st.write(
        "**Dados encontrados:**",
        "Sim" if resultado["tem_dados"] else "Não"
    )

    st.info(resultado["detalhes"])

    with st.expander("Ver resultado técnico completo"):
        st.json(resultado)

st.divider()

st.header("🧭 Próximas análises")

st.info(
    "O próximo passo será ampliar os testes para outras "
    "APIs brasileiras e investigar autenticação, limites, "
    "atualização dos dados, gratuidade e uso comercial."
)

st.caption(
    "RADAR DE OPORTUNIDADES | Nova arquitetura | Versão 1.1"
)
