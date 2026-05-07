#codigo errado
@app.get("/usuarios/{id}")
def buscar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    return usuario


#codigo certo
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True

@app.get("/usuarios/{id}", response_model=UsuarioResponse)
def buscar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise UsuarioNaoEncontrado(f"Usuário {id} não encontrado")
    return usuario

#se o usuario nao existir o .first() retorna None.
#retornar None diretamente faz o FastAPI serializar como null ou causar erro 500.
#o cliente nao recebe uma mensagem clara do que aconteceu.
#sobre o que pode vazar do banco
#o codigo errado retorna o objeto ORM diretamente.
#o objeto ORM pode conter campos sensiveis como senha, token, data de criacao interna.
#sem um schema de resposta (Pydantic), todos os campos do modelo sao expostos.
#o certo seria ter um UsuarioResponse com apenas os campos que o cliente pode ver.