#codigo errado
def get_usuario_atual(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    usuario_id = payload.get("sub")
    return buscar_usuario(usuario_id)

#codigo certo
async def get_usuario_atual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        usuario_id = payload.get("sub")
        return await buscar_usuario(usuario_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")  
#a funcao errada nao tem o tratamento de excecao para o caso do token estar expirado, entao se o usuario tentar usar um token expirado ele recebera um erro generico
#a funcao de tratam,ento deve estar em um handler e esse codigo deve tratar o erro mas nao lancar httpException, pois a camada de service nao deve saber sobre http, entao criei uma excecao personalizada para o caso do token estar expirado e lancei ela no service, e depois no handler eu trato essa excecao e lanço o HTTPException com o status code e detalhe apropriado.exception
#apenas avisar o aqruivo handler que houve um problem e ele se responsabilizar em achar
