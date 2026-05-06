#função errada
@app.get("/documentos")
async def listar_documentos():
    import time
    time.sleep(2)
    docs = db.find_all()
    return docs

#função correta
@app.get("/documentos")
async def listar_documentos():
    import time
    await time.sleep(2)
    docs = await db.find_all()
    return docs

#como a funcao e async ela roda dentro do event loop.
#o .sleep() trava a thread inteira assim parando o event loop que e single thread
#entao precisa usar o await assim o event loop pode continuar com outra requisicao
#e volta depois de um tempo determinado dentro do sleep
#o await no db.find_all() tem a mesma funcao do await no sleep, se nao tivesse o python
#precisaria esperar toda a requisicao da recuperacao do banco acabar para poder continuar com outras requisicoes
#agora caso o banco tenha muito volume o certo seria colocar paginacao

#funcao com paginacao
@app.get("/documentos")
async def listar_documentos(pagina: int = 1, tamanho: int = 10):
    import time

    offset = (pagina - 1) * tamanho

    query = select([documentos]).offset(offset).limit(tamanho)

    await time.sleep(2)
    docs = await db.execute(query)
    return docs

#o calculo do offset e para poder pular os registros anterios 
#o pagina -1 e para fazer o offset comecar do zero, pu seja, desde o comeco dos resgistro assum qundo ele retornar os 10
#ele pula para o 11 e retorna ate o 20
#linha 32  e: seleciona os documentos com o offset e limite de 10 por retorno
#e os awaits liberam o eventlopp enquanto o banco nao retorna os 10 registros 


