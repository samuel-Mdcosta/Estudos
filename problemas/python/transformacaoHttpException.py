# handler.py — único que converte para HTTP
@app.exception_handler(UsuarioNaoEncontrado)
def handler(request, exc):
    raise HTTPException(status_code=404, detail="Usuário não encontrado")
