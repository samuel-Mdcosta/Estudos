# Middleware de autenticacao JWT com FastAPI
# Fluxo: toda requisicao passa pelo middleware antes de chegar na rota.
# O middleware verifica se o token JWT e valido. Se sim, injeta os dados
# do usuario na request e deixa passar. Se nao, retorna 401 imediatamente.

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
import jwt  # biblioteca PyJWT: decodifica e valida tokens JWT

app = FastAPI()

# Chave secreta usada para assinar e verificar os tokens JWT.
# Em producao, isso deve vir de uma variavel de ambiente (ex: os.getenv("SECRET_KEY"))
SECRET_KEY = "minha_chave_secreta"

# Algoritmo de assinatura do token. HS256 usa a SECRET_KEY como chave simetrica,
# ou seja, a mesma chave assina e verifica.
ALGORITHM = "HS256"

# Lista de rotas que nao exigem autenticacao.
# O middleware deixa essas rotas passarem sem verificar token.
# /docs e /openapi.json sao as rotas da documentacao automatica do FastAPI.
ROTAS_PUBLICAS = ["/login", "/registro", "/docs", "/openapi.json"]

# Esquema de seguranca do tipo Bearer Token.
# Usado principalmente para que o Swagger UI (/docs) exiba o campo de autenticacao.
security = HTTPBearer()


def verificar_token(token: str) -> dict:
    # Tenta decodificar o token usando a SECRET_KEY e o algoritmo definido.
    # jwt.decode ja valida a assinatura e a expiracao automaticamente.
    # Retorna o payload (dicionario com os dados que foram colocados no token).
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        # O token existe e e valido, mas o campo "exp" ja passou da hora atual.
        raise HTTPException(status_code=401, detail="Token expirado")

    except jwt.InvalidTokenError:
        # Cobre qualquer outro problema: assinatura errada, token malformado, etc.
        raise HTTPException(status_code=401, detail="Token invalido")


# O decorator @app.middleware("http") registra essa funcao para interceptar
# TODA requisicao HTTP antes de ela chegar em qualquer rota da aplicacao.
# A funcao recebe a request e o call_next, que e o proximo passo na cadeia
# (pode ser outro middleware ou a rota final).
@app.middleware("http")
async def middleware_autenticacao(request: Request, call_next):

    # Se o caminho da requisicao estiver na lista de rotas publicas,
    # chama call_next diretamente, pulando toda a logica de autenticacao.
    if request.url.path in ROTAS_PUBLICAS:
        return await call_next(request)

    # Busca o header "Authorization" da requisicao.
    # O padrao Bearer Token e: Authorization: Bearer <token>
    authorization = request.headers.get("Authorization")

    # Se o header nao existir ou nao comecar com "Bearer ", rejeita a requisicao.
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"detail": "Token nao fornecido"}
        )

    # Extrai apenas o token, removendo o prefixo "Bearer ".
    # Ex: "Bearer abc123" -> "abc123"
    token = authorization.split(" ")[1]

    try:
        # Valida o token. Se for invalido ou expirado, levanta HTTPException.
        payload = verificar_token(token)

        # Injeta o payload do token em request.state.usuario.
        # request.state e um espaco livre para armazenar dados durante a requisicao.
        # Assim, qualquer rota pode acessar os dados do usuario via request.state.usuario
        # sem precisar decodificar o token novamente.
        request.state.usuario = payload

    except HTTPException as e:
        # Captura os erros lancados por verificar_token e retorna como JSON.
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    # Token valido: passa a requisicao para a rota correspondente.
    return await call_next(request)


# --- Rotas de exemplo ---

@app.post("/login")
async def login():
    import datetime

    # Em producao, aqui voce validaria o usuario e senha recebidos no body
    # contra o banco de dados. Nesse exemplo, o login e sempre bem-sucedido.

    # Cria o payload do token com:
    # "sub" (subject): identificador do usuario, convencao do padrao JWT
    # "role": papel do usuario, usado para controle de acesso nas rotas
    # "exp": data/hora de expiracao do token (1 hora a partir de agora)
    token = jwt.encode(
        {
            "sub": "usuario123",
            "role": "admin",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # Retorna o token para o cliente. O cliente deve guardar esse token
    # e enviar em toda requisicao futura no header: Authorization: Bearer <token>
    return {"access_token": token, "token_type": "bearer"}


@app.get("/perfil")
async def perfil(request: Request):
    # Essa rota so e alcancada se o middleware ja validou o token.
    # Os dados do usuario estao disponiveis em request.state.usuario,
    # que foi preenchido pelo middleware com o payload do JWT.
    usuario = request.state.usuario
    return {"mensagem": f"Bem-vindo, {usuario['sub']}", "role": usuario["role"]}


@app.get("/admin")
async def admin(request: Request):
    usuario = request.state.usuario

    # Autenticacao (token valido) ja foi garantida pelo middleware.
    # Aqui fazemos AUTORIZACAO: verifica se o usuario tem permissao de admin.
    # Autenticacao = "voce e quem diz ser?"
    # Autorizacao  = "voce tem permissao para isso?"
    if usuario.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")

    return {"mensagem": "Area administrativa liberada"}
