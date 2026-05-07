#codigo errado
@app.post("/chunks")
async def salvar_chunk(chunk: dict):
    await db.chunks.insert_one(chunk)
    return {"ok": True}

#codigo certo
class validarChunck(BaseModel):
    nome: str
    textos: str
    embedding: list[float] = []

@app.post("/chuncks")
async def salvar_chuncks(Chunk: validarChunck) -> validarChunck:
    await db.chuncks.insert_one(Chunk.model_dump())
    return Chunk

#uma insercao sem validacao pode fazer com que o usuario use nosql injection
#a validação tambem serve para a rota saber o que ta sendo inserido, caso fosse ujma rota get ela saberia o q deve buscar

