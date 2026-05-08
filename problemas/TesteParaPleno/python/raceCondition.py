#codigo errado
contador_requisicoes = 0

@app.middleware("http")
async def contar(request, call_next):
    global contador_requisicoes
    contador_requisicoes += 1
    return await call_next(request)

#codigo certo
import redis.asyncio as redis

r = redis.Redis()

@app.middleware("http")
async def contar(request, call_next):
    await r.incr("contador_requisicoes")
    return await call_next(request)


# --- POR QUE O CÓDIGO ERRADO É PROBLEMÁTICO? ---
#
# Imagine um placar de gols num estádio com 4 operadores (workers).
# Cada operador tem o placar na cabeça e atualiza quando alguém marca.
#
# Se dois gols são marcados ao mesmo tempo, os dois operadores leem o placar (ex: 2 gols),
# os dois somam 1, e os dois escrevem 3. O placar marca 3, mas deveriam ser 4.
# Um gol sumiu.
#
# É exatamente isso que acontece com "contador += 1" em memória:
# são 3 passos (ler, somar, salvar) e dois workers podem executar esses passos
# ao mesmo tempo, fazendo um sobrescrever o resultado do outro.


# --- POR QUE A SOLUÇÃO COM REDIS FOI ESCOLHIDA? ---
#
# O Redis é como um placar oficial centralizado, fora do estádio,
# que só aceita um update por vez. Não importa quantos operadores existam,
# todos mandam a mensagem "soma 1" para o mesmo lugar,
# e o Redis processa uma de cada vez, na ordem que chegaram.
#
# O comando INCR do Redis é atômico por natureza: leitura, soma e escrita
# acontecem em um único passo indivisível. Race condition impossível.
#
# asyncio.Lock foi descartado porque só funciona dentro de um único processo.
# Com múltiplos workers (Gunicorn, Kubernetes), cada processo tem seu próprio lock
# e seu próprio contador na memória, o que não resolve nada.
# O Redis resolve para qualquer número de workers em qualquer número de máquinas.
