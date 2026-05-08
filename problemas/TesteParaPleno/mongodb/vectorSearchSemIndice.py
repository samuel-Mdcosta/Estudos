#codigo errado
pipeline = [
    {"$match": {"status": "ativo"}},
    {"$lookup": {
        "from": "usuarios",
        "localField": "usuario_id",
        "foreignField": "_id",
        "as": "usuario"
    }},
    {"$limit": 20}
]

# codigo certo
db.sua_colecao.create_index("status")
db.sua_colecao.create_index("usuario_id")

pipeline = [
    {"$match": {"status": "ativo"}},
    {"$lookup": {
        "from": "usuarios",
        "localField": "usuario_id",
        "foreignField": "_id",
        "as": "usuario"
    }},
    {"$limit": 20}
]

# --- POR QUE O CÓDIGO ERRADO É PROBLEMÁTICO? ---
#
# Imagine uma biblioteca com milhares de livros sem nenhuma organização.
# Para achar todos os livros de um autor, um funcionário precisa pegar livro por livro
# e verificar um a um — mesmo que só 3 livros sejam desse autor.
#
# O $match sem índice faz exatamente isso: varre TODOS os documentos da coleção
# para filtrar os que têm status = "ativo", mesmo que sejam poucos.
#
# Depois, o $lookup sem índice em usuario_id é ainda pior:
# para CADA documento que passou pelo $match, o MongoDB vai até a coleção "usuarios"
# e varre ela inteira procurando o usuário correspondente.
# Se passaram 1000 documentos no $match, são 1000 varreduras completas em "usuarios".


# --- POR QUE OS ÍNDICES RESOLVEM? ---
#
# Um índice é como o fichário de uma biblioteca: organizado e separado,
# permite pular direto para o que você procura sem olhar os outros.
#
# O índice em "status" faz o $match pular direto para os documentos ativos,
# sem tocar nos inativos.
#
# O índice em "usuario_id" faz o $lookup pular direto para o usuário correto
# em vez de varrer a coleção inteira a cada join.
#
# O _id de "usuarios" já tem índice automático no MongoDB, por isso
# só precisamos criar os dois índices na coleção de origem.
