#funcao errada
import time
from urllib import response


@app.get("/processos")
async def listar_processos(db: Session = Depends(get_db)):
    return db.query(Processo).all()

#funcao correta
@app.get("/processos")
async def listar_processos(db: Session = Depends(get_db), pagina: int = 1, tamanhao: int = 10):

    offset = (pagina - 1) * tamanhao

    query = select([processos]).offset(offset).limit(tamanhao)

    await time.sleep(2)
    reponse = await db.execute(query)

    return response