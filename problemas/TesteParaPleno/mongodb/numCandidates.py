#codigo errado
pipeline = [{
    "$vectorSearch": {
        "index": "vector_index",
        "path": "embedding",
        "queryVector": query_embedding,
        "numCandidates": 5,
        "limit": 5
    }
}]

#codigo certo
pipeline = [{
    "$vectorSearch": {
        "index": "vector_index",
        "path": "embedding",
        "queryVector": query_embedding,
        "numCandidates": 50,
        "limit": 5
    }
}]

#o numero de num cadidates sempre deve ser maior que limite, assim o indice 
#passa por mais vetores no grafo
