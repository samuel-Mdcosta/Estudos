#codigo errado
@app.post("/documentos")
def criar_documento(dados):
    return db.inserir(dados)

#codigo certo
class criarDados(BaseModel):
    titulo: str
    conteudo: str
    usuario_id: str

@app.post("/documentos")
async def criar_documento(dados: criarDados) -> criarDados:
    return db.inserir(dados)

#a tiipagem e o tipo que a rota espera receber e retornar 
#isso evita a rota receber dados errados como um int no lugar de uma string
#a funcao estava errada por que nao validava os dados que recebia nem os dados que retornava


