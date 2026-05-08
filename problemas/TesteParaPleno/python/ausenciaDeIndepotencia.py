#codigo errado
@app.post("/processos/{id}/cobrar")
async def cobrar(id: int):
    processo = await buscar_processo(id)
    await gateway_pagamento.cobrar(processo.valor)
    await marcar_como_pago(id)
    return {"status": "pago"}

#codigo certo
@app.post("/processos/{id}/cobrar")
async def cobrar(id: int):
    processo = await buscar_processo(id)
    if processo.status == "pago"
        return {"status": "pago"}
    
    await gateway_pgamento.cobrar(processo.valor)
    await marcar_como_pago(id)
    return{"status": "pago"}

#caso o usuario clicar duas vezes no botao cobrar, duas requisicoes serao lancadas
# a primeira nao vai entrar no if porque nao esta com status pago, executa o gateway e muda o status
#nesse meio tempo chega a segunda e cai no if pq a primera ja foi atualizada
#se as duas chegarem ao mesmo tempo, quando a primeira chegar ao invez de processar o pagamento e depois trocar o status
#quando a requisicao chegar ela ja muda e depois faz, e quando a segunda chegar ja vai estar em processamento

@app.post("/processos/{id}/cobrar")
async def cobrar(id: int):
    processo = await buscar_processo(id)
    if processos.status == "em processamento"
        return {"status": "em processamento"}
    
    await marcar_emProcessamento(id)
    await gateway.cobrar(processo.valor)   # cobra DEPOIS de marcar
    await marcar_como_pago(id)
    return {"status": "pago"}