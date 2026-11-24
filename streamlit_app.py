
import streamlit as st

from fontes_mercado import listar_fontes, fontes_publicas
from motor_pncp import buscar_contratacoes_abertas
from analisador_oportunidades import analisar_contratacoes


# --------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Radar de Oportunidades",
    page_icon="📡",
    layout="wide"
)


# --------------------------------------------------
# CABEÇALHO
# --------------------------------------------------

st.title("📡 RADAR DE OPORTUNIDADES")

st.caption(
    "Inteligência de negócios digitais | Mercado brasileiro"
)


# --------------------------------------------------
# INDICADORES
# --------------------------------------------------

fontes = listar_fontes()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Fontes cadastradas",
    len(fontes)
)

col2.metric(
    "Fontes públicas",
    len(fontes_publicas())
)

col3.metric(
    "Oportunidades investigadas",
    0
)


st.divider()


# --------------------------------------------------
# INVESTIGAÇÃO NO PNCP
# --------------------------------------------------

st.header("🏛️ Investigação de contratações públicas")

st.write(
    "Pesquise contratações públicas e identifique "
    "necessidades que possam indicar oportunidades "
    "para soluções digitais."
)

uf = st.selectbox(
    "Estado para pesquisar",
    [
        "Todos",
        "RS",
        "SC",
        "PR",
        "SP",
        "RJ",
        "MG",
        "BA",
        "GO",
        "DF"
    ]
)


if st.button(
    "🔍 Buscar e analisar oportunidades",
    type="primary"
):

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

            if not analises:
                st.info(
                    "Os registros foram recebidos, mas nenhum "
                    "objeto de contratação pôde ser classificado."
                )

            for item in analises:

                titulo = (
                    f"{item['categoria']} | "
                    f"{item['ocorrencias']} ocorrências"
                )

                with st.expander(titulo):

                    st.metric(
                        "Pontuação exploratória",
                        f"{item['pontuacao_exploratoria']}/100"
                    )

                    st.write(
                        "**Sinais de soluções digitais:**",
                        item["sinais_digitais"]
                    )

                    st.write(
                        "**Interpretação:**",
                        item["interpretacao"]
                    )

                    st.write("**Exemplos encontrados:**")

                    for exemplo in item["exemplos"]:
                        st.write(f"• {exemplo}")

            st.warning(
                "A pontuação é experimental. A frequência de "
                "contratações não comprova demanda comercial, "
                "rentabilidade ou disposição para pagar."
            )

            with st.expander("Consultar registros originais"):

                for registro in registros:
                    st.json(registro)

        else:

            st.info(
                "Nenhuma contratação foi encontrada nessa consulta."
            )

    else:

        st.error(
            resultado.get(
                "erro",
                "Não foi possível consultar o PNCP."
            )
        )


st.divider()


# --------------------------------------------------
# FONTES DE INTELIGÊNCIA
# --------------------------------------------------

st.header("🌐 Fontes de inteligência")

for fonte in fontes:

    with st.expander(fonte["nome"]):

        st.write(
            "**Categoria:**",
            fonte["categoria"]
        )

        st.write(
            "**Descrição:**",
            fonte["descricao"]
        )

        st.write(
            "**Acesso:**",
            fonte["acesso"]
        )

        st.link_button(
            "Consultar fonte",
            fonte["url"]
        )


# --------------------------------------------------
# RODAPÉ
# --------------------------------------------------

st.divider()

st.caption(
    "RADAR DE OPORTUNIDADES | Versão 0.4"
)
