from sqlalchemy.orm import Session
from app.models import Usuario, Notificacao

#objeto da otificacao (dict)
async def notificar_usuario(
    usuario_id: int,
    tipo: str,
    dados: dict,
    db: Session
):
    # busca com ORM — sem SQL puro
    #pareciso com eloquente do laravel
    #retorna usuario pelo id, assim nao precisa da query:
    #"INSERT INTO notificacoes (usuario_id, tipo, dados) VALUES (:uid, :tipo, :dados)",
    #{"uid": usuario_id, "tipo": tipo, "dados": json.dumps(dados)}
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    #se nao encontrar o usuario, loga o erro e retorna sem tentar enviar push ou salvar notificacao
    if not usuario:
        logger.error(f"Usuário {usuario_id} não encontrado")
        return

    # envia push
    await push_service.enviar(
        token=usuario.push_token,
        titulo=TEMPLATES[tipo]["titulo"],
        corpo=TEMPLATES[tipo]["corpo"].format(**dados)
    )

    # salva com ORM — sem SQL puro
    #armazena a notificacao no banco, para que o usuario possa ver o historico de notificacoes
    notificacao = Notificacao(
        usuario_id=usuario_id,
        tipo=tipo,
        dados=dados
    )
    db.add(notificacao)
    db.commit()