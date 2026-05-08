#codigo errado
def get_db():
    db = SessionLocal()
    return db  # sem yield, sem fechar

@app.get("/processos")
def listar(db: Session = Depends(get_db)):
    return db.query(Processo).all()

#codigo certo

class processosRequest(BaseModel):
    nome: str
    id: int
    processo: list[str] = []

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/processos", reponse_model=list[processosRequest])
async def listar(db: Session = Depends(get_db)):
    return db.query(Processos).all()
