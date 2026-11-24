
FONTES = [
    {
        "nome": "PNCP",
        "categoria": "Compras públicas",
        "publico": "Empresas e fornecedores",
        "descricao": "Editais, contratos, atas e planos de contratação.",
        "url": "https://www.gov.br/pncp/pt-br/acesso-a-informacao/dados-abertos",
        "acesso": "Consulta pública",
        "potencial": "Identificar demandas de órgãos públicos",
        "status": "Documentado"
    },
    {
        "nome": "Consumidor.gov.br",
        "categoria": "Problemas de consumidores",
        "publico": "Consumidores e empresas",
        "descricao": "Reclamações, respostas e resolução de conflitos.",
        "url": "https://consumidor.gov.br/pages/principal/documentacao-api",
        "acesso": "Credenciais necessárias",
        "potencial": "Identificar problemas recorrentes",
        "status": "Acesso restrito"
    }
]


def listar_fontes():
    return FONTES


def contar_fontes():
    return len(FONTES)


def fontes_por_categoria(categoria):
    return [
        fonte for fonte in FONTES
        if fonte["categoria"] == categoria
    ]


def fontes_publicas():
    return [
        fonte for fonte in FONTES
        if fonte["acesso"] == "Consulta pública"
    ]

