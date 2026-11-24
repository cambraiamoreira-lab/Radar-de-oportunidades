
import streamlit as st

from fontes_mercado import listar_fontes, fontes_publicas
from motor_pncp import buscar_contratacoes_abertas
from analisador_oportunidades import analisar_contratacoes

st.set_page_config(
    page_title="Radar de Oportunidades",
    page_icon="📡",
    layout="wide"
)

st.title("📡 RADAR DE OPORTUNIDADES")
st.caption("Inteligência de negócios digitais | Mercado brasileiro")

fontes = listar_fontes()

col1, col2, col3 = st.columns(3)
col1.metric("Fontes cadastradas", len(fontes))
col2.metric("Fontes públicas", len(fontes_publicas()))
col3.metric("Oportunidades investigadas", 0)

st.divider()

st.header("🏛️ Investigação de contratações públicas")

uf = st.selectbox(
    "Estado para pesquisar",
    ["Todos", "RS", "SC", "PR", "SP", "RJ", "MG", "BA", "GO", "DF"]
)

if st.button("🔍 Buscar e analisar oportunidades", type="primary):

    with st.spinner("Consultando o PNCP..."):
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

            analises = analisar_contratacoes(registros)

            st.header("🧠 Inteligência de mercado")

            st.write(
                f"Categorias identificadas: {len(analises)}"
            )

            for item in analises:

                with st.expander(
                    f"{item['categoria']} | "
                    f"{item['ocorrencias']} ocorrências"
                ):

                    st.metric(
                        "Pontuação exploratória",
                        f"{item['pontuacao_exploratoria']}/100"
                    )

                    st.write(
                        "**Sinais de soluções digitais:**",
                        item["sinais_digitais"]
                    )

                    st.write("**Interpretação:**", item["interpretacao"])

                    st.write("**Exemplos encontrados:**")

                    for exemplo in item["exemplos"]:
                        st.write(f"• {exemplo}")

            st.warning(
                "A pontuação é experimental. Frequência de compras "
                "não comprova demanda comercial nem disposição para pagar."
            )

            with st.expander("Consultar registros originais"):
                for registro in registros:
                    st.json(registro)

        else:
            st.info("Nenhuma contratação encontrada.")

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

st.caption("RADAR DE OPORTUNIDADES | Versão 0.4")
