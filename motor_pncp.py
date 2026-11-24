
import requests
from datetime import datetime


URL_BASE = "https://pncp.gov.br/api/consulta"
ENDPOINT = f"{URL_BASE}/v1/contratacoes/proposta"


def buscar_contratacoes_abertas(
    modalidade=6,
    uf=None,
    pagina=1,
    tamanho_pagina=20
):
    """
    Consulta contratações com recebimento de propostas aberto.
    Modalidade 6 = Pregão Eletrônico.
    """

    data_final = datetime.now().strftime("%Y%m%d")

    parametros = {
        "dataFinal": data_final,
        "codigoModalidadeContratacao": modalidade,
        "pagina": pagina,
        "tamanhoPagina": tamanho_pagina
    }

    if uf:
        parametros["uf"] = uf.upper()

    try:
        resposta = requests.get(
            ENDPOINT,
            params=parametros,
            headers={"Accept": "application/json"},
            timeout=30
        )

        resposta.raise_for_status()
        dados = resposta.json()

        if isinstance(dados, list):
            registros = dados
        else:
            registros = dados.get("data", [])

        return {
            "sucesso": True,
            "quantidade": len(registros),
            "registros": registros,
            "resposta_original": dados,
            "erro": None
        }

    except requests.exceptions.Timeout:
        return {
            "sucesso": False,
            "quantidade": 0,
            "registros": [],
            "erro": "Tempo limite de conexão com o PNCP."
        }

    except requests.exceptions.RequestException as erro:
        return {
            "sucesso": False,
            "quantidade": 0,
            "registros": [],
            "erro": f"Erro de comunicação: {erro}"
        }

    except ValueError:
        return {
            "sucesso": False,
            "quantidade": 0,
            "registros": [],
            "erro": "O PNCP retornou uma resposta inválida."
        }


def testar_conexao():
    resultado = buscar_contratacoes_abertas()

    if resultado["sucesso"]:
        return {
            "status": "Conectado",
            "registros_encontrados": resultado["quantidade"]
        }

    return {
        "status": "Falha",
        "erro": resultado["erro"]
    }
