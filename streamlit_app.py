
import streamlit as st

from catalogo_apis import (
    listar_apis,
    listar_segmentos
)

from verificador_apis import (
    testar_banco_central,
    testar_portal_dados_abertos
)


st.set_page_config(
    page_title="Radar de Oportunidades",
    page_icon="🔎",
    layout="wide"
)


st.title("🔎 RADAR DE OPORTUNIDADES")

st.markdown(
    """
    **Descubra APIs brasileiras, dados abertos
    e oportunidades para criar soluções digitais.**

    Nosso objetivo é identificar dados reais que possam
    gerar automações, ferramentas e novos negócios.
    """
)

st.divider()


# VISÃO GERAL

apis_catalogadas = listar_apis()
segmentos = listar_segmentos()

st.subheader("📊 Visão geral do catálogo")

col1, col2 = st.columns(2)

with col1:
    st.metric("APIs catalogadas", len(apis_catalogadas))

with col2:
    st.metric("Segmentos identificados", len(segmentos))


# CATÁLOGO

st.divider()

st.subheader("📚 Catálogo de APIs brasileiras")

filtro = st.selectbox(
    "Filtrar por segmento",
    ["Todos"] + segmentos
)

apis_exibidas = apis_catalogadas

if filtro != "Todos":
    apis_exibidas = [
        api for api in apis_catalogadas
        if api.get("segmento") == filtro
    ]

for api in apis_exibidas:

    with st.expander(api.get("nome", "API sem nome")):

        st.write("**Órgão responsável:**",
                 api.get("orgao", "Não informado"))

        st.write("**Segmento:**",
                 api.get("segmento", "Não informado"))

        st.write("**Descrição:**",
                 api.get("descricao", "Não informada"))

        st.write("**Dados disponíveis:**",
                 api.get("dados_disponiveis", "Não informado"))

        st.write("**Aplicações possíveis:**",
                 api.get("aplicacoes_hipoteticas", "Não informadas"))

        st.write("**Modelo de acesso:**",
                 api.get("modelo_acesso", "A investigar"))

        st.write("**Chave de acesso:**",
                 api.get("requer_chave", "A verificar"))

        st.write("**Gratuidade:**",
                 api.get("gratuita", "A verificar"))

        st.write("**Uso comercial:**",
                 api.get("uso_comercial", "A verificar"))

        st.write("**Situação:**",
                 api.get("status", "Não verificada"))

        documentacao = api.get("documentacao_url")
        acesso = api.get("url_acesso")

        if documentacao:
            st.markdown(
                f"[📖 Documentação]({documentacao})"
            )

        if acesso:
            st.markdown(
                f"[🌐 Acessar fonte]({acesso})"
            )


# LABORATÓRIO

st.divider()

st.header("🧪 Laboratório de testes")

st.write(
    "Verifique a resposta técnica das APIs "
    "e se elas retornam dados."
)


def exibir_resultado(resultado):

    st.write("**Status:**", resultado["status"])

    st.write(
        "**Código HTTP:**",
        resultado["codigo_http"]
    )

    st.write(
        "**Tempo de resposta:**",
        resultado["tempo_resposta"],
        "segundos"
    )

    st.write(
        "**Formato recebido:**",
        resultado["formato"]
    )

    st.write(
        "**Dados encontrados:**",
        "Sim" if resultado["tem_dados"] else "Não"
    )

    st.write("**Detalhes:**", resultado["detalhes"])

    with st.expander("Visualizar resposta técnica"):
        st.json(resultado)


# BANCO CENTRAL

st.subheader("🏦 Banco Central do Brasil")

if st.button("🚀 Testar API do Banco Central"):

    with st.spinner("Consultando Banco Central..."):

        resultado = testar_banco_central()

    exibir_resultado(resultado)


# PORTAL DE DADOS ABERTOS

st.subheader("📂 Portal Brasileiro de Dados Abertos")

if st.button("🚀 Testar Portal de Dados Abertos"):

    with st.spinner("Consultando Portal de Dados Abertos..."):

        resultado = testar_portal_dados_abertos()

    exibir_resultado(resultado)


# RODAPÉ

st.divider()

st.caption("Radar de Oportunidades | Versão 1.2")
