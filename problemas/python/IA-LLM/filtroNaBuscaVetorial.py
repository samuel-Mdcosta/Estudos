#codigo errado
resultados = atlas.aggregate([{
    "$vectorSearch": {
        "index": "vector_index",
        "path": "embedding",
        "queryVector": query_embedding,
        "numCandidates": 50,
        "limit": 5
        # sem filtro de usuário/documento
    }
}])

#codigo errado
resultados = atlas.aggregate([{
    "$vectorSearch": {
        "index": "vector_index",
        "path": "embedding",
        "queryVector": query_embedding,
        "numCandidates": 50,
        "limit": 5,
        "filter": {
            "usuario_id": usuario_id
        }
    }
}])

#o filtro dentro do codigo de vector seach faz com que a busca atue dobre um grupo especifico
#se nao tiver quando um ussuairo especifico fazer uma pergunta a busca vai retornar repostad de outros usuairos
#com o filtro a busca vai retornar apenas os resultados relacionados ao usuario_id especifico, garantindo que as respostas sejam mais relevantes e personalizadas para aquele usuário.