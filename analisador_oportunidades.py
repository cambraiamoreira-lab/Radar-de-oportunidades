
import re
import unicodedata
from collections import defaultdict


# ==================================================
# 1. CATEGORIAS DE NECESSIDADES
# ==================================================

CATEGORIAS = {
    "Tecnologia e sistemas": [
        "software",
        "aplicativo",
        "plataforma digital",
        "sistema informatizado",
        "desenvolvimento de sistema",
        "tecnologia da informacao",
        "informatica",
        "banco de dados",
        "api",
        "hospedagem de sistemas",
        "licenca de uso"
    ],

    "Gestao e processos": [
        "gestao",
        "administracao",
        "controle",
        "processo",
        "consultoria",
        "assessoria",
        "gerenciamento",
        "organizacao",
        "planejamento"
    ],

    "Manutencao e infraestrutura": [
        "manutencao",
        "reparo",
        "instalacao",
        "infraestrutura",
        "construcao",
        "reforma",
        "poda",
        "arborizacao",
        "equipamento"
    ],

    "Saude": [
        "saude",
        "medicamento",
        "hospital",
        "clinica",
        "exame",
        "medico",
        "odontologico",
        "material medico",
        "equipamento hospitalar"
    ],

    "Educacao": [
        "educacao",
        "escola",
        "ensino",
        "material didatico",
        "treinamento",
        "capacitacao",
        "pedagogico"
    ],

    "Transporte e logistica": [
        "transporte",
        "veiculo",
        "logistica",
        "frete",
        "combustivel",
        "entrega",
        "mobilidade"
    ],

    "Alimentacao": [
        "alimentacao",
        "alimento",
        "merenda",
        "refeicao",
        "generos alimenticios"
    ],

    "Meio ambiente": [
        "meio ambiente",
        "residuos",
        "arborizacao",
        "vegetacao",
        "saneamento",
        "reciclagem",
        "preservacao ambiental"
    ]
}


# ==================================================
# 2. INDICADORES DIGITAIS
# ==================================================

# Expressões que indicam contratação digital
# de maneira mais explícita.

INDICADORES_DIGITAIS_FORTES = [
    "desenvolvimento de software",
    "desenvolvimento de sistema",
    "sistema informatizado",
    "licenciamento de software",
    "licenca de uso de software",
    "plataforma digital",
    "aplicativo",
    "banco de dados",
    "desenvolvimento de aplicacao",
    "automacao de processos",
    "servico de tecnologia da informacao",
    "solucao tecnologica",
    "api de integracao",
    "hospedagem de sistemas",
    "software de gestao"
]


# Infraestrutura e serviços digitais.
# São sinais relevantes, mas não necessariamente
# indicam desenvolvimento de um novo produto.

INDICADORES_DIGITAIS_MODERADOS = [
    "computacao em nuvem",
    "armazenamento em nuvem",
    "seguranca da informacao",
    "servico de rede de computadores",
    "infraestrutura de ti",
    "servidor de dados",
    "suporte de sistemas",
    "integracao de sistemas",
    "processamento de dados",
    "servicos de informatica"
]


# Equipamentos físicos de informática.
# Não devem ser confundidos com software.

INDICADORES_HARDWARE = [
    "computador",
    "notebook",
    "microcomputador",
    "monitor",
    "impressora",
    "servidor",
    "equipamento de informatica",
    "periferico",
    "estacao de trabalho"
]


# ==================================================
# 3. NORMALIZAÇÃO
# ==================================================

def normalizar(texto):
    texto = str(texto or "").lower()

    texto = unicodedata.normalize(
        "NFKD",
        texto
    )

    texto = "".join(
        letra
        for letra in texto
        if not unicodedata.combining(letra)
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()


# ==================================================
# 4. EXTRAÇÃO DO OBJETO
# ==================================================

def extrair_objeto(registro):

    if not isinstance(registro, dict):
        return ""

    campos = [
        "objetoCompra",
        "objeto",
        "descricao",
        "descricaoObjeto"
    ]

    for campo in campos:

        valor = registro.get(campo)

        if isinstance(valor, str) and valor.strip():
            return valor.strip()

    return ""


# ==================================================
# 5. IDENTIFICAÇÃO DE CATEGORIAS
# ==================================================

def identificar_categorias(objeto):

    texto = normalizar(objeto)

    encontradas = []

    for categoria, palavras in CATEGORIAS.items():

        for palavra in palavras:

            if normalizar(palavra) in texto:

                encontradas.append(categoria)
                break

    if not encontradas:
        encontradas.append("Outras necessidades")

    return encontradas


# ==================================================
# 6. NATUREZA DA CONTRATAÇÃO
# ==================================================

def identificar_natureza(objeto):

    texto = normalizar(objeto)

    indicadores_produto = [
        "aquisicao",
        "fornecimento",
        "compra",
        "material permanente",
        "equipamento"
    ]

    indicadores_servico = [
        "prestacao de servico",
        "contratacao de empresa",
        "execucao de servicos",
        "servicos especializados",
        "manutencao",
        "consultoria",
        "assessoria"
    ]

    produto = any(
        termo in texto
        for termo in indicadores_produto
    )

    servico = any(
        termo in texto
        for termo in indicadores_servico
    )

    if produto and servico:
        return "Produto e serviço"

    if produto:
        return "Produto ou equipamento"

    if servico:
        return "Prestação de serviço"

    return "Natureza não identificada"


# ==================================================
# 7. IDENTIFICAÇÃO DE COMPONENTE DIGITAL
# ==================================================

def identificar_componente_digital(objeto):

    texto = normalizar(objeto)

    fortes = [
        termo
        for termo in INDICADORES_DIGITAIS_FORTES
        if normalizar(termo) in texto
    ]

    moderados = [
        termo
        for termo in INDICADORES_DIGITAIS_MODERADOS
        if normalizar(termo) in texto
    ]

    hardware = [
        termo
        for termo in INDICADORES_HARDWARE
        if normalizar(termo) in texto
    ]

    if fortes:

        return {
            "classificacao": "Digital explícito",
            "nivel_evidencia": "Forte",
            "indicadores": fortes,
            "hardware": hardware,
            "pontuacao": 100
        }

    if moderados:

        return {
            "classificacao": "Infraestrutura ou serviço digital",
            "nivel_evidencia": "Moderado",
            "indicadores": moderados,
            "hardware": hardware,
            "pontuacao": 60
        }

    if hardware:

        return {
            "classificacao": "Equipamento de informática",
            "nivel_evidencia": "Hardware",
            "indicadores": [],
            "hardware": hardware,
            "pontuacao": 0
        }

    return {
        "classificacao": "Sem evidência digital identificada",
        "nivel_evidencia": "Não identificado",
        "indicadores": [],
        "hardware": [],
        "pontuacao": 0
    }


# ==================================================
# 8. INTERPRETAÇÃO
# ==================================================

def interpretar_oportunidade(componente, natureza):

    nivel = componente["nivel_evidencia"]

    if nivel == "Forte":

        return (
            "Investigar mercado, concorrentes e possíveis "
            "soluções digitais relacionadas à contratação."
        )

    if nivel == "Moderado":

        return (
            "Investigar se existe demanda por serviços "
            "ou ferramentas digitais complementares."
        )

    if nivel == "Hardware":

        return (
            "Aquisição de equipamentos identificada. "
            "Não há evidência de demanda por software."
        )

    if natureza == "Prestação de serviço":

        return (
            "Necessidade de serviço identificada. "
            "Investigar se existe possibilidade de "
            "digitalização ou automação."
        )

    return (
        "Necessidade identificada. Investigar o mercado "
        "antes de formular uma hipótese de negócio."
    )


# ==================================================
# 9. ANÁLISE DAS CONTRATAÇÕES
# ==================================================

def analisar_contratacoes(registros):

    grupos = defaultdict(list)

    total_validos = 0

    for registro in registros:

        objeto = extrair_objeto(registro)

        if not objeto:
            continue

        total_validos += 1

        categorias = identificar_categorias(objeto)

        natureza = identificar_natureza(objeto)

        componente = identificar_componente_digital(objeto)

        interpretacao = interpretar_oportunidade(
            componente,
            natureza
        )

        analise = {
            "objeto": objeto,
            "categorias": categorias,
            "natureza": natureza,
            "componente_digital": componente["classificacao"],
            "nivel_evidencia": componente["nivel_evidencia"],
            "indicadores_digitais": componente["indicadores"],
            "equipamentos_informatica": componente["hardware"],
            "pontuacao_exploratoria": componente["pontuacao"],
            "interpretacao": interpretacao
        }

        for categoria in categorias:
            grupos[categoria].append(analise)

    resultados = []

    for categoria, itens in grupos.items():

        digitais_fortes = sum(
            1
            for item in itens
            if item["nivel_evidencia"] == "Forte"
        )

        digitais_moderados = sum(
            1
            for item in itens
            if item["nivel_evidencia"] == "Moderado"
        )

        hardware = sum(
            1
            for item in itens
            if item["nivel_evidencia"] == "Hardware"
        )

        exemplos = []

        vistos = set()

        for item in itens:

            chave = normalizar(item["objeto"])

            if chave not in vistos:

                exemplos.append(item)

                vistos.add(chave)

            if len(exemplos) >= 5:
                break

        # A pontuação representa somente a proporção
        # de registros com evidência digital.
        # Não representa potencial comercial.

        if itens:

            pontuacao = round(
                100 * (
                    digitais_fortes +
                    digitais_moderados * 0.6
                ) / len(itens)
            )

        else:
            pontuacao = 0

        resultados.append({

            "categoria": categoria,

            "ocorrencias": len(itens),

            "sinais_digitais": (
                digitais_fortes + digitais_moderados
            ),

            "sinais_digitais_fortes": digitais_fortes,

            "sinais_digitais_moderados": digitais_moderados,

            "equipamentos_informatica": hardware,

            "pontuacao_exploratoria": pontuacao,

            "exemplos": [
                item["objeto"]
                for item in exemplos
            ],

            "detalhes": exemplos,

            "interpretacao": (
                "Existem evidências digitais explícitas. "
                "Investigar o mercado."
                if digitais_fortes > 0
                else
                "Existem sinais de infraestrutura digital. "
                "Investigar a necessidade."
                if digitais_moderados > 0
                else
                "Não foram identificadas evidências digitais "
                "suficientes nesta categoria."
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


# ==================================================
# 10. RESUMO GERAL
# ==================================================

def resumo_analise(registros):

    resultados = analisar_contratacoes(registros)

    total_validos = sum(
        item["ocorrencias"]
        for item in resultados
    )

    return {

        "total_analisado": len(registros),

        "total_registros_validos": total_validos,

        "categorias_identificadas": len(resultados),

        "resultados": resultados

    }
