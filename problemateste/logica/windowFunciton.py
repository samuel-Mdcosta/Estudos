import sqlite3
import textwrap

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.executescript("""
    CREATE TABLE vendas (
        id          INTEGER PRIMARY KEY,
        vendedor_id INTEGER NOT NULL,
        produto     TEXT    NOT NULL,
        valor       REAL    NOT NULL,
        data        TEXT    NOT NULL   -- ISO: YYYY-MM-DD
    );

    INSERT INTO vendas VALUES
    --  id  vid  produto   valor    data
        (1,  1, 'Notebook', 3200, '2024-01-05'),
        (2,  1, 'Monitor',  1500, '2024-01-18'),
        (3,  1, 'Teclado',   350, '2024-01-22'),
        (4,  2, 'Notebook', 2800, '2024-01-10'),
        (5,  2, 'Mouse',     200, '2024-01-15'),
        (6,  3, 'Monitor',  1800, '2024-01-08'),
        (7,  3, 'Notebook', 3100, '2024-01-20'),
        (8,  1, 'SSD',       900, '2024-02-03'),
        (9,  1, 'Notebook', 3500, '2024-02-14'),
        (10, 2, 'Monitor',  1600, '2024-02-07'),
        (11, 2, 'Notebook', 3000, '2024-02-19'),
        (12, 2, 'Teclado',   400, '2024-02-25'),
        (13, 3, 'Mouse',     180, '2024-02-11'),
        (14, 3, 'SSD',       750, '2024-02-28');
""")

# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------

QUERIES = {

    # 1. Rank dos vendedores por total de vendas dentro de cada mês
    #
    # Primeiro agrega o total por (mês, vendedor) numa CTE, depois aplica
    # RANK() sobre a partição do mês ordenada pelo total decrescente.
    # RANK() repete o número quando há empate e pula o próximo
    # (use DENSE_RANK() se quiser sem pulos).
    "1. Rank por total mensal": """
        WITH totais AS (
            SELECT vendedor_id,
                   strftime('%Y-%m', data) AS mes,
                   SUM(valor)              AS total
            FROM   vendas
            GROUP  BY vendedor_id, mes
        )
        SELECT mes,
               vendedor_id,
               total,
               RANK() OVER (
                   PARTITION BY mes
                   ORDER BY     total DESC
               ) AS rank_mes
        FROM  totais
        ORDER BY mes, rank_mes
    """,

    # 2. Segunda maior venda de cada vendedor
    #
    # DENSE_RANK() sobre as vendas individuais de cada vendedor.
    # Filtrar rank = 2 retorna a(s) venda(s) no segundo valor mais alto.
    # Se o vendedor tiver apenas 1 valor distinto, nenhuma linha aparece.
    "2. Segunda maior venda por vendedor": """
        WITH ranked AS (
            SELECT *,
                   DENSE_RANK() OVER (
                       PARTITION BY vendedor_id
                       ORDER BY     valor DESC
                   ) AS rnk
            FROM  vendas
        )
        SELECT vendedor_id, id AS venda_id, produto, valor
        FROM   ranked
        WHERE  rnk = 2
        ORDER  BY vendedor_id
    """,

    # 3. Percentual de cada venda sobre o total do vendedor
    #
    # SUM(valor) OVER (PARTITION BY vendedor_id) calcula o total do vendedor
    # sem colapsar as linhas, permitindo dividir cada venda pelo seu total.
    "3. Percentual de cada venda no total do vendedor": """
        SELECT id AS venda_id,
               vendedor_id,
               produto,
               valor,
               ROUND(
                   valor * 100.0 /
                   SUM(valor) OVER (PARTITION BY vendedor_id),
               2) AS pct_do_total
        FROM  vendas
        ORDER BY vendedor_id, valor DESC
    """,

    # 4. Vendedores com crescimento >= 20% em relação ao mês anterior
    #
    # CTE totais: agrega por (vendedor, mês).
    # LAG(total) OVER (PARTITION BY vendedor ORDER BY mês) busca o total
    # do mês anterior na mesma partição sem nenhum JOIN extra.
    # Filtra onde total_atual >= total_anterior * 1.20.
    "4. Vendedores com crescimento >= 20% sobre o mes anterior": """
        WITH totais AS (
            SELECT vendedor_id,
                   strftime('%Y-%m', data) AS mes,
                   SUM(valor)              AS total
            FROM   vendas
            GROUP  BY vendedor_id, mes
        ),
        com_lag AS (
            SELECT vendedor_id,
                   mes,
                   total                                          AS total_atual,
                   LAG(total) OVER (
                       PARTITION BY vendedor_id
                       ORDER BY     mes
                   )                                             AS total_anterior
            FROM   totais
        )
        SELECT vendedor_id,
               mes,
               total_atual,
               total_anterior,
               ROUND((total_atual - total_anterior) * 100.0
                     / total_anterior, 1) AS crescimento_pct
        FROM   com_lag
        WHERE  total_anterior IS NOT NULL
          AND  total_atual >= total_anterior * 1.20
        ORDER  BY crescimento_pct DESC
    """,
}

# ---------------------------------------------------------------------------
# Exibicao
# ---------------------------------------------------------------------------

def print_results(title: str, query: str) -> None:
    print(f"\n{'=' * 65}")
    print(f" {title}")
    print(f"{'=' * 65}")
    sql = textwrap.dedent(query).strip()
    for line in sql.splitlines():
        print(f"  {line}")
    print()
    rows = cur.execute(query).fetchall()
    if not rows:
        print("  (sem resultados)")
        return
    headers = list(rows[0].keys())
    col_w = {h: max(len(str(h)), max(len(str(r[h] or '')) for r in rows))
             for h in headers}
    sep = "  " + "  ".join("-" * col_w[h] for h in headers)
    print("  " + "  ".join(str(h).ljust(col_w[h]) for h in headers))
    print(sep)
    for row in rows:
        print("  " + "  ".join(str(row[h] or '').ljust(col_w[h]) for h in headers))


if __name__ == "__main__":
    for title, sql in QUERIES.items():
        print_results(title, sql)
    print()
