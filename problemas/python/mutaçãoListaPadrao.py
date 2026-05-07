#codigo errado
def adicionar_documento(doc, lista=[]):
    lista.append(doc)
    return lista

print(adicionar_documento("doc1"))
print(adicionar_documento("doc2"))

#codigo certo
def adicionar_documento(doc, lista = None):
    if lista is None:
        lista = []
    lista.append(doc)
    return lista

#mutação de lista padrao é quando usa um elemento que pode ser mutavel como valor padrao do parametro
#quando a funcao e chamada ela cria valores padrao uma unica vez, nao a cada chamada
#entao toda chamada vai ser a mesma lista assim adicionando o mesmo documento a mesma lista, e nao criando uma nova lista a cada chamada
# entao a solucao e usar none e fazer a verificacao dentro da funcao para criar uma nova lista a cada chamada, evitando a mutacao da lista padrao.
#a cada chamada a lista cresce com o mesmo decoumento e indefinidamente a cada inovacao
