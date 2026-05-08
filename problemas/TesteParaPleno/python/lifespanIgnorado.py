#codigo errado
modelo_nlp = None

@app.get("/analisar")
async def analisar(texto: str):
    global modelo_nlp
    if modelo_nlp is None:
        modelo_nlp = spacy.load("pt_core_news_lg")  # 800MB
    return modelo_nlp(texto)


#codigo certo
modelo_nlp = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global modelo_nlp
    modelo_nlp = spacy.load("pt_core_news_lg")  # carrega UMA vez, no startup
    yield
    modelo_nlp = None  # cleanup no shutdown

app = FastAPI(lifespan=lifespan)

@app.get("/analisar")
async def analisar(texto: str):
    return modelo_nlp(texto)  # modelo já está pronto, sem if/lazy load


# --- POR QUE O CÓDIGO ERRADO É PROBLEMÁTICO? ---
#
# Imagine que você tem uma padaria com 4 atendentes (workers).
# O modelo de NLP é como uma máquina de café pesada (800MB) que precisa ser ligada antes de usar.
#
# No código errado, nenhum atendente liga a máquina quando chega ao trabalho.
# Cada um só vai ligar quando o PRIMEIRO cliente pedir café.
#
# Problema 1 - DEMORA SURPRESA:
#   O primeiro cliente de cada atendente vai esperar a máquina inteira ligar (pode demorar minutos).
#   Os outros clientes na fila ficam parados esperando sem entender o porquê.
#
# Problema 2 - CAOS NA ABERTURA:
#   Se 4 clientes chegam ao mesmo tempo logo que a padaria abre,
#   os 4 atendentes tentam ligar a máquina ao mesmo tempo.
#   Isso pode travar ou até quebrar a máquina por sobrecarga.


# --- POR QUE O CÓDIGO CERTO RESOLVE? ---
#
# No código certo, usando o "lifespan" do FastAPI, é como definir uma regra:
# "Antes de abrir a padaria para os clientes, TODOS os atendentes ligam a máquina."
#
# Só depois que a máquina estiver pronta, a porta da padaria é aberta.
# Nenhum cliente espera, nenhum atendente briga pelo botão de ligar.
#
# O health check no Docker é como um segurança na porta:
# ele só deixa os clientes entrarem depois de confirmar que a máquina já está ligada.
# Isso é útil quando a padaria abre uma filial nova (novo servidor subindo),
# garantindo que a filial não receba clientes antes de estar 100% pronta.
