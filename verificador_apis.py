
import requests
import time


def testar_api(url, parametros=None, timeout=20):
    """
    Testa uma API e verifica:
    - Se o servidor responde
    - Código HTTP
    - Tempo de resposta
    - Tipo de conteúdo
    - Se retorna JSON válido
    - Se existem dados na resposta
    """

    inicio = time.time()

    resultado = {
        "url": url,
        "status": "Não testada",
        "codigo_http": None,
        "tempo_resposta": None,
        "formato": None,
        "tem_dados": False,
        "detalhes": ""
    }

    try:
        resposta = requests.get(
            url,
            params=parametros,
            timeout=timeout,
            headers={
                "User-Agent": "RadarDeOportunidades/1.0"
            }
        )

        tempo = round(time.time() - inicio, 2)

        resultado["codigo_http"] = resposta.status_code
        resultado["tempo_resposta"] = tempo

        resposta.raise_for_status()

        tipo = resposta.headers.get(
            "Content-Type", ""
        ).lower()

        if "json" in tipo:
            dados = resposta.json()
            resultado["formato"] = "JSON"

            if isinstance(dados, (dict, list)):
                resultado["tem_dados"] = len(dados) > 0

            resultado["status"] = "Acessível"

            resultado["detalhes"] = (
                "A API respondeu e retornou JSON válido."
            )

        else:
            resultado["formato"] = tipo or "Não identificado"

            resultado["status"] = "Resposta recebida"

            resultado["detalhes"] = (
                "O servidor respondeu, mas não confirmou "
                "retorno em JSON."
            )

        if not resposta.content:
            resultado["tem_dados"] = False

    except requests.exceptions.Timeout:
        resultado["status"] = "Tempo esgotado"
        resultado["detalhes"] = (
            "A API demorou mais que o limite permitido."
        )

    except requests.exceptions.HTTPError as erro:
        resultado["status"] = "Erro HTTP"
        resultado["detalhes"] = str(erro)

    except requests.exceptions.ConnectionError:
        resultado["status"] = "Falha de conexão"
        resultado["detalhes"] = (
            "Não foi possível estabelecer conexão."
        )

    except ValueError:
        resultado["status"] = "JSON inválido"
        resultado["detalhes"] = (
            "A resposta não contém JSON válido."
        )

    except requests.exceptions.RequestException as erro:
        resultado["status"] = "Erro na requisição"
        resultado["detalhes"] = str(erro)

    except Exception as erro:
        resultado["status"] = "Erro inesperado"
        resultado["detalhes"] = str(erro)

    return resultado


def testar_banco_central():
    """
    Testa uma série histórica do Banco Central:
    cotação de compra do dólar.
    """

    url = (
        "https://api.bcb.gov.br/dados/serie/"
        "bcdata.sgs.1/dados/ultimos/5"
    )

    parametros = {
        "formato": "json"
    }

    return testar_api(url, parametros)


def classificar_resultado(resultado):

    if (
        resultado["status"] == "Acessível"
        and resultado["tem_dados"]
    ):
        return "API ACESSÍVEL COM DADOS"

    if resultado["status"] == "Acessível":
        return "API ACESSÍVEL, SEM DADOS"

    return "NECESSITA INVESTIGAÇÃO"


def testar_lista_apis(lista_urls):

    resultados = []

    for item in lista_urls:

        resultado = testar_api(item["url"])

        resultado["nome"] = item["nome"]

        resultado["classificacao"] = (
            classificar_resultado(resultado)
        )

        resultados.append(resultado)

    return resultados
      
