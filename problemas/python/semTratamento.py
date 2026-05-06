#codigo errado
@app.get("/dashboard")
async def dashboard():
    usuarios = await buscar_usuarios()
    pedidos = await buscar_pedidos()
    receita = await buscar_receita()
    return {"usuarios": usuarios, "pedidos": pedidos, "receita": receita}

#codigo certo
@app.get("/dashboard")
async def dashboard():
    resultado = await asyncio.gather(
        buscar_usuarios(),
        buscar_pedidos(),
        buscar_receita(),
        return_exceptions=True
    )
    usuarios, pedidos, receita = resultado
    return {"usuarios": usuarios, "pedidos": pedidos, "receita": receita}

#a funcao errada, certamente teria um problema com a demora, pois somaria o tempo de requisicao de todas apis
#entao coloquei um ayncio.gather para que as tres fossem resolvidas ao memsmo tempo assim so ldemoranvo o  tempo da mais demorafa
#adicionei u return_exception para que se alguma reuisicao desse problema nao parace todas assim a que deu errado poderia ser tratada depois
# e adicionei uma desestruturacao dos resultados para melhor legibilidade do dicionario