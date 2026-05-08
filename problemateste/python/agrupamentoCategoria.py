"""
Você tem uma lista de dicionários onde cada item representa um documento com os campos tipo e valor_causa. 
Escreva uma função que agrupe os documentos por tipo e retorne, para cada tipo, a quantidade de documentos e a soma total dos valores de causa.
"""

def agrupar(docs):
    from collections import defaultdict
    groups = defaultdict(lambda: {'quantidade': 0, 'soma': 0})
    for doc in docs:
        tipo = doc['tipo']
        valor = doc['valor_causa']
        groups[tipo]['quantidade'] += 1
        groups[tipo]['soma'] += valor
    return dict(groups)


documentos = [
    {"tipo": "contrato", "valor_causa": 15000},
    {"tipo": "peticao",  "valor_causa": 8000},
    {"tipo": "contrato", "valor_causa": 22000},
    {"tipo": "recurso",  "valor_causa": 5000},
    {"tipo": "peticao",  "valor_causa": 12000},
]

resultado = agrupar(documentos)

for tipo, dados in resultado.items():
    print(f"{tipo}: {dados['quantidade']} doc(s), soma R${dados['soma']:,.2f}")
