#codigo errado
@app.get("/usuarios/{id}")
def buscar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    return usuario


#codigo certo
@app.get("/usuarios/{id}")
def buscar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise UsuarioNaoEncontrado(f"Usuário {id} não encontrado")
    return usuario