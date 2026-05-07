#codigo errado
# Na indexação:
embedder = NomicEmbedder(model="nomic-embed-text-v1")
chunks_indexados = embedder.embed(chunks)
salvar_no_atlas(chunks_indexados)

# Na busca:
embedder2 = OpenAIEmbedder(model="text-embedding-3-small")
query_embedding = embedder2.embed(pergunta_usuario)
resultados = atlas.buscar(query_embedding)

#codigo certo
# Na indexação:
embedder = NomicEmbedder(model="nomic-embed-text-v1")
chunks_indexados = embedder.embed(chunks)
salvar_no_atlas(chunks_indexados)

# Na busca:
embedder2 = OpenAIEmbedder(model="nomic-embed-text-v1")
query_embedding = embedder2.embed(pergunta_usuario)
resultados = atlas.buscar(query_embedding)

#o erro estava na utilização de modelos de embedding diferentes
#modelos podotem ter difentes modos de fazer embedagem, entao a comparacao entre o resultados dos modelos podem levar a resultados invalidos
