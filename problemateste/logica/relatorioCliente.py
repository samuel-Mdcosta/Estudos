import sqlite3
import textwrap

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.executescript("""
    CREATE TABLE clientes (
        id    INTEGER PRIMARY KEY,
        nome  TEXT NOT NULL,
        cidade TEXT NOT NULL
    );

    CREATE TABLE pedidos (
        id          INTEGER PRIMARY KEY,
        cliente_id  INTEGER REFERENCES clientes(id),
        valor       REAL NOT NULL,
        data        TEXT NOT NULL,
        status      TEXT NOT NULL  -- 'pago' | 'pendente' | 'cancelado'
    );

    INSERT INTO clientes VALUES
        (1, 'Ana Lima',    'São Paulo'),
        (2, 'Bruno Souza', 'Rio de Janeiro'),
        (3, 'Carla Dias',  'Belo Horizonte'),
        (4, 'Diego Reis',  'Curitiba'),       -- nunca pediu
        (5, 'Eva Nunes',   'Fortaleza');      -- nunca pediu

    INSERT INTO pedidos VALUES
        (1,  1,  500.00, '2024-01-10', 'pago'),
        (2,  1,  700.00, '2024-02-15', 'pago'),
        (3,  2,  300.00, '2024-01-20', 'pago'),
        (4,  2,  200.00, '2024-03-05', 'pendente'),
        (5,  3, 1200.00, '2024-02-28', 'pago'),
        (6,  3,  150.00, '2024-04-01', 'cancelado'),
        (7,  1,   80.00, '2024-04-10', 'pendente');
""")

# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------

QUERIES = {

    # 1. Clientes que fizeram pelo menos um pedido
    # JOIN garante apenas clientes com linha correspondente em pedidos;
    # DISTINCT evita duplicatas quando há múltiplos pedidos.
    "1. Clientes com pelo menos um pedido": """
        SELECT DISTINCT c.id, c.nome, c.cidade
        FROM   clientes c
        JOIN   pedidos  p ON p.cliente_id = c.id
        ORDER  BY c.nome
    """,

    # 2. Clientes que NUNCA fizeram pedido
    # LEFT JOIN + filtro NULL: linhas sem correspondência em pedidos ficam com p.id = NULL.
    "2. Clientes sem nenhum pedido": """
        SELECT c.id, c.nome, c.cidade
        FROM   clientes c
        LEFT JOIN pedidos p ON p.cliente_id = c.id
        WHERE  p.id IS NULL
        ORDER  BY c.nome
    """,

    # 3. Valor total de pedidos por cliente (maior → menor)
    # SUM agrega todos os pedidos independente de status.
    "3. Total de pedidos por cliente (maior para menor)": """
        SELECT   c.nome,
                 c.cidade,
                 SUM(p.valor)        AS total,
                 COUNT(p.id)         AS qtd_pedidos
        FROM     clientes c
        JOIN     pedidos  p ON p.cliente_id = c.id
        GROUP BY c.id
        ORDER BY total DESC
    """,

    # 4. Clientes cuja soma de pedidos PAGOS ultrapassa R$ 1.000,00
    # HAVING filtra após o GROUP BY; o WHERE restringe apenas pedidos 'pago'
    # antes da agregação, o que é mais eficiente do que filtrar no HAVING.
    "4. Clientes com total de pedidos pagos > R$ 1.000,00": """
        SELECT   c.nome,
                 c.cidade,
                 SUM(p.valor) AS total_pago
        FROM     clientes c
        JOIN     pedidos  p ON p.cliente_id = c.id
        WHERE    p.status = 'pago'
        GROUP BY c.id
        HAVING   total_pago > 1000
        ORDER BY total_pago DESC
    """,
}

# ---------------------------------------------------------------------------
# Exibição
# ---------------------------------------------------------------------------

def print_results(title: str, query: str) -> None:
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print('=' * 60)
    print(f"SQL:{textwrap.indent(textwrap.dedent(query).strip(), '  ')}")
    print()
    rows = cur.execute(query).fetchall()
    if not rows:
        print("  (sem resultados)")
        return
    headers = rows[0].keys()
    col_w = {h: max(len(h), max(len(str(r[h])) for r in rows)) for h in headers}
    header_line = "  " + "  ".join(h.ljust(col_w[h]) for h in headers)
    print(header_line)
    print("  " + "-" * (len(header_line) - 2))
    for row in rows:
        print("  " + "  ".join(str(row[h]).ljust(col_w[h]) for h in headers))


if __name__ == "__main__":
    for title, sql in QUERIES.items():
        print_results(title, sql)
    print()
