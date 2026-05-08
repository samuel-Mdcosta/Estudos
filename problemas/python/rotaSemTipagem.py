#codigo errado
@app.post("/documentos")
def criar_documento(dados):
    return db.inserir(dados)

#codigo certo
class criarDados(BaseModel):
    titulo: str
    conteudo: str
    usuario_id: str

@app.post("/documentos", response_model=criarDados)
async def criar_documento(dados: criarDados) -> criarDados:
    return db.inserir(dados)

# POR QUE E UM PROBLEMA:
# Sem tipagem, a rota aceita qualquer coisa em dados — o FastAPI nao valida nem o que
# entra nem o que sai. Um int no lugar de uma string passa sem erro, e o retorno do
# db.inserir() vai cru para o cliente, podendo expor campos internos do banco.

# POR QUE A SOLUCAO FUNCIONA:
# A tipagem dados: criarDados faz o FastAPI validar o corpo da requisicao antes de
# executar a funcao — se um campo estiver errado ou faltando, retorna 422 automaticamente.
# O response_model=criarDados controla o que volta na resposta: o FastAPI serializa
# o retorno do db.inserir() pelo schema, garantindo que apenas os campos declarados
# em criarDados aparecem na resposta — sem vazar campos extras do banco.


