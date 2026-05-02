#um generator yield e uma funcao que se parece com uma fila, onde vai sendo executado conforme cioloca nela
#o yield executa uma acao por vez no modo lazy, so executa quando necessario ou quando pedido com next()

async def buscar1miusuarios(base_url: str):
    pagina = 1 
    while True:
        async with httpx.AsyncClient() as client:
            #define o limite de usuarios por pagina
            response = await client.get(f"{base_url}/usuarios", params={"pagina": pagina, limite: 100})
            dados = response.json()

            #se a resposta tiver itens, entao retorna os itens, senao, para o loop
            if not dados["itens"]:
                break

            for usuario in dados["itens"]:
                #para os usuarios que tem os dados dentro dew itens
                #percorre e retorna um por um, para evitar estouro de memoria
                yield usuario

            if not dados["tem_proxima_pagina"]:
                break
            
            pagina += 1
