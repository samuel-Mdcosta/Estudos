--codigo errado
-- e retornado todos os usuarios da tabela e armazenados em usuarios
--depois e feito um loop para percorrer e contar todos os pedidos relacionados ao id do usuairo
-- assim o sistema faz uma query + n queys para cada usuario
usuarios = db.query(Usuario).all()

for usuario in usuarios:
    pedidos = db.query(Pedido).filter(
        Pedido.usuario_id == usuario.id
    ).all()
    print(usuario.nome, len(pedidos))

--codigo certo
-- Uma única query com JOIN agrega os pedidos por usuário no banco.
-- O COUNT conta os pedidos de cada usuário e o GROUP BY agrupa por usuario.
-- Resultado: 1 query no lugar de N+1.
resultado = db.execute("""
    SELECT u.nome, COUNT(p.id) as total_pedidos
    FROM usuarios u
    LEFT JOIN pedidos p ON p.usuario_id = u.id
    GROUP BY u.id, u.nome
""").fetchall()

for row in resultado:
    print(row.nome, row.total_pedidos)

--codigo certo com sqlalchemy orm
-- func.count e o equivalente do COUNT do SQL no ORM.
-- outerjoin e o equivalente do LEFT JOIN.
-- group_by agrupa por usuario, igual ao GROUP BY.
-- O ORM monta e executa uma unica query, sem loop no banco.
from sqlalchemy import func

resultado = (
    db.query(Usuario.nome, func.count(Pedido.id).label("total_pedidos"))
    .outerjoin(Pedido, Pedido.usuario_id == Usuario.id)
    .group_by(Usuario.id, Usuario.nome)
    .all()
)

for row in resultado:
    print(row.nome, row.total_pedidos)
