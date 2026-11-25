
import streamlit as st

from catalogo_apis import (
    listar_apis,
    listar_segmentos,
    resumo_catalogo
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


# PAINEL DO CATÁLOGO

st.subheader("📊 Visão geral do catálogo")

resumo = resumo_catalogo()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "APIs catalogadas",
        contar_apis_seguro()
    )

with col2:
    st.metric(
        "Segmentos identificados",
        len(listar_segmentos())
    )

with col3:
    st.metric(
        "Fontes em investigação",
        len(listar_apis())
    )


# CATÁLOGO

st.divider()

st.subheader("📚 Catálogo de APIs brasileiras")

segmentos = ["Todos"] + listar_segmentos()

segmento_escolhido = st.selectbox(
    "Filtrar por segmento",
    segmentos
)

apis = listar_apis()

if segmento_escolhido != "Todos":
    apis = [
        api for api in apis
        if api.get("segmento") == segmento_escolhido
    ]

for api in apis:

    with st.expander(api.get("nome", "API sem nome")):

        st.write(
            "**Órgão responsável:**",
            api.get("orgao", "Não informado")
        )

        st.write(
            "**Segmento:**",
            api.get("segmento", "Não informado")
        )

        st.write(
            "**Descrição:**",
            api.get("descricao", "Não informada")
        )

        st.write(
            "**Dados disponíveis:**",
            api.get("dados_disponiveis", "Não informado")
        )

        st.write(
            "**Aplicações possíveis:**",
            api.get("aplicacoes_hipoteticas", "Não informadas")
        )

        st.write(
            "**Acesso:**",
            api.get("modelo_acesso", "A investigar")
        )

        st.write(
            "**Chave de acesso:**",
            api.get("requer_chave", "A verificar")
        )

        st.write(
            "**Gratuidade:**",
            api.get("gratuita", "A verificar")
        )

        st.write(
            "**Uso comercial:**",
            api.get("uso_comercial", "A verificar")
        )

        st.write(
            "**Situação:**",
            api.get("status", "Não verificada")
        )

        if api.get("documentacao"):
            st.markdown(
                f"[📖 Documentação]({api['documentacao']})"
            )

        if api.get("url_acesso"):
            st.markdown(
                f"[🌐 Acessar fonte]({api['url_acesso']})"
            )


# LABORATÓRIO DE TESTES

st.divider()

st.header("🧪 Laboratório de testes")

st.write(
    "Teste a disponibilidade técnica das APIs "
    "e verifique se elas retornam dados."
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

    st.write(
        "**Detalhes:**",
        resultado["detalhes"]
    )

    with st.expander("Visualizar resposta técnica"):
        st.json(resultado)


# TESTE BANCO CENTRAL

st.subheader("🏦 Banco Central do Brasil")

if st.button("🚀 Testar API do Banco Central"):

    with st.spinner("Consultando Banco Central..."):

        resultado = testar_banco_central()

    exibir_resultado(resultado)


# TESTE PORTAL DE DADOS ABERTOS

st.subheader("📂 Portal Brasileiro de Dados Abertos")

if st.button("🚀 Testar Portal de Dados Abertos"):

    with st.spinner("Consultando Portal de Dados Abertos..."):

        resultado = testar_portal_dados_abertos()

    exibir_resultado(resultado)


# RODAPÉ

st.divider()

st.caption(
    "Radar de Oportunidades | Versão 1.2"
)


# FUNÇÃO AUXILIAR

def contar_apis_seguro():
    return len(listar_apis())
