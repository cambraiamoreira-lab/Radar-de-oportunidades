
import streamlit as st
from fontes_mercado import listar_fontes, fontes_publicas
from motor_pncp import buscar_contratacoes_abertas

st.set_page_config(
    page_title="Radar de Oportunidades",
    page_icon="📡",
    layout="wide"
)

st.title("📡 RADAR DE OPORTUNIDADES")
st.caption("Inteligência para descobrir negócios digitais no Brasil.")

fontes = listar_fontes()

col1, col2, col3 = st.columns(3)
col1.metric("Fontes cadastradas", len(fontes))
col2.metric("Fontes públicas", len(fontes_publicas()))
col3.metric("Oportunidades validadas", 0)

st.divider()

st.header("🔎 Investigação de mercado")
st.write(
    "Estamos investigando necessidades reais de órgãos públicos "
    "para identificar possíveis oportunidades de negócios."
)

st.subheader("🏛️ Radar de contratações públicas")

uf = st.selectbox(
    "Estado para pesquisar",
    ["Todos", "RS", "SC", "PR", "SP", "RJ", "MG", "BA", "GO", "DF"]
)

if st.button("🔍 Buscar contratações no PNCP", type="primary"):
    with st.spinner("Consultando dados públicos do PNCP..."):
        resultado = buscar_contratacoes_abertas(
            uf=None if uf == "Todos" else uf,
            tamanho_pagina=20
        )

    if resultado["sucesso"]:
        registros = resultado["registros"]

        st.success(
            f"Consulta concluída: {len(registros)} registros recebidos."
        )

        if registros:
            st.subheader("Contratações encontradas")

            for i, registro in enumerate(registros, 1):
                objeto = registro.get("objetoCompra", "Objeto não informado")
                orgao = registro.get("orgaoEntidade", {})
                
                if isinstance(orgao, dict):
                    nome_orgao = orgao.get(
                        "razaoSocial", "Órgão não identificado"
                    )
                else:
                    nome_orgao = str(orgao)

                valor = registro.get("valorTotalEstimado")

                with st.expander(f"{i}. {objeto}"):
                    st.write("**Órgão:**", nome_orgao)
                    st.write(
                        "**Valor estimado:**",
                        f"R$ {valor:,.2f}" if isinstance(valor, (int, float))
                        else "Não informado"
                    )
                    st.json(registro)
        else:
            st.info("Nenhuma contratação foi retornada nesta consulta.")
    else:
        st.error(resultado["erro"])

st.divider()

st.header("🌐 Fontes de inteligência")

for fonte in fontes:
    with st.expander(fonte["nome"]):
        st.write("**Categoria:**", fonte["categoria"])
        st.write("**Descrição:**", fonte["descricao"])
        st.write("**Acesso:**", fonte["acesso"])
        st.link_button("Consultar fonte", fonte["url"])

st.divider()

st.caption("RADAR DE OPORTUNIDADES | Versão 0.3")
