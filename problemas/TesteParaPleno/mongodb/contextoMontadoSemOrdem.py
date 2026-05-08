#codigo errado
chunks = buscar_chunks_similares(pergunta, top_k=5)
contexto = "\n".join([c["texto"] for c in chunks])
prompt = f"Responda com base no contexto:\n{contexto}\n\nPergunta: {pergunta}"

#codigo certo
chunks = buscar_chunks_similares(pergunta, top_k=5)
chunks_ordenados = sorted(chunks, key=lambda c: c["posicao"])
contexto = "\n".join([c["texto"] for c in chunks_ordenados])
prompt = f"Responda com base no contexto:\n{contexto}\n\nPergunta: {pergunta}"


# --- POR QUE O CÓDIGO ERRADO É PROBLEMÁTICO? ---
#
# Problema 1 - Chunks fora de ordem:
# Imagine ler um contrato onde o artigo 10 aparece antes do artigo 2.
# O vector search retorna os trechos por similaridade com a pergunta,
# não pela ordem que aparecem no documento original.
# Em textos jurídicos isso é grave: uma cláusula pode dizer "conforme disposto no item 3.1"
# mas o item 3.1 aparece depois no contexto enviado para a LLM,
# quebrando o raciocínio e podendo gerar respostas erradas.
#
# Problema 2 - Chunks sem sobreposição (overlap):
# Se o documento foi dividido em pedaços sem overlap,
# uma frase que começa no fim do chunk 3 e termina no início do chunk 4
# chega cortada ao modelo. Em linguagem jurídica, onde uma vírgula
# pode mudar o sentido de uma obrigação, isso é crítico.


# --- POR QUE A TRATATIVA RESOLVE? ---
#
# O sorted() por "posicao" reordena os chunks pela posição original no documento
# antes de montar o contexto. A LLM recebe o texto na sequência lógica,
# como se estivesse lendo o documento de verdade.
#
# Para resolver o problema de overlap, ao indexar o documento os chunks devem
# ser criados com sobreposição (ex: 100 tokens de overlap entre chunks consecutivos),
# garantindo que nenhuma frase seja cortada ao meio.
# Isso é configurado na etapa de chunking, antes de salvar no MongoDB.
