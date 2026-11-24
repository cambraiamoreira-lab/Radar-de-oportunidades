
import re
import unicodedata
from collections import Counter, defaultdict


CATEGORIAS = {
    "Tecnologia e sistemas": [
        "software", "sistema", "aplicativo", "plataforma",
        "informatica", "tecnologia", "digital", "dados",
        "programa", "licenca", "desenvolvimento"
    ],
    "Gestao e processos": [
        "gestao", "administracao", "controle", "processo",
        "consultoria", "assessoria", "gerenciamento",
        "organizacao", "planejamento"
    ],
    "Manutencao e infraestrutura": [
        "manutencao", "reparo", "instalacao", "equipamento",
        "infraestrutura", "construcao", "reforma"
    ],
    "Saude": [
        "saude", "medicamento", "hospital", "clinica",
        "exame", "medico", "odontologico"
    ],
    "Educacao": [
        "educacao", "escola", "ensino", "material didatico",
        "treinamento", "capacitação"
    ],
    "Transporte e logistica": [
        "transporte", "veiculo", "logistica", "frete",
        "combustivel", "entrega"
    ],
    "Alimentacao": [
        "alimentacao", "alimento", "merenda", "refeicao",
        "generos alimenticios"
    ]
}

INDICADORES_DIGITAIS = [
    "software", "sistema", "aplicativo", "plataforma",
    "digital", "automacao", "informatica", "dados",
    "processamento", "monitoramento", "gestao"
]


def normalizar(texto):
    texto = str(texto or "").lower()

    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(
        letra for letra in texto
        if not unicodedata.combining(letra)
    )

    return re.sub(r"\s+", " ", texto).strip()


def identificar_categoria(objeto):
    texto = normalizar(objeto)

    for categoria, palavras in CATEGORIAS.items():
        for palavra in palavras:
            if normalizar(palavra) in texto:
                return categoria

    return "Outras necessidades"


def analisar_contratacoes(registros):
    grupos = defaultdict(list)

    for registro in registros:
        objeto = registro.get("objetoCompra", "")

        if not objeto:
            continue

        categoria = identificar_categoria(objeto)
        grupos[categoria].append(objeto)

    resultados = []

    for categoria, objetos in grupos.items():
        exemplos = list(dict.fromkeys(objetos))[:5]
        quantidade = len(objetos)

        sinais = sum(
            1 for objeto in objetos
            if any(
                palavra in normalizar(objeto)
                for palavra in INDICADORES_DIGITAIS
            )
        )

        pontuacao = min(
            100,
            quantidade * 10 + sinais * 15
        )

        resultados.append({
            "categoria": categoria,
            "ocorrencias": quantidade,
            "sinais_digitais": sinais,
            "pontuacao_exploratoria": pontuacao,
            "exemplos": exemplos,
            "interpretacao": (
                "Investigar possível solução digital"
                if sinais > 0
                else "Investigar a necessidade e o mercado"
            )
        })

    resultados.sort(
        key=lambda item: (
            item["pontuacao_exploratoria"],
            item["ocorrencias"]
        ),
        reverse=True
    )

    return resultados


def resumo_analise(registros):
    resultados = analisar_contratacoes(registros)

    return {
        "total_analisado": len(registros),
        "categorias_identificadas": len(resultados),
        "resultados": resultados
    }

