-- PROBLEMA: Query sem índice
-- Sem índice nas colunas do WHERE, o PostgreSQL executa um full table scan:
-- varre todas as linhas da tabela para aplicar o filtro e depois ordena o resultado.
-- Em tabelas com muitos registros isso é lento e consome muita memória.
SELECT * FROM processos
WHERE status = 'ativo'
AND created_at > '2024-01-01'
ORDER BY created_at DESC;

-- SOLUÇÃO: Índice composto nas colunas filtradas
-- Um índice é uma estrutura auxiliar que o PostgreSQL mantém separada da tabela.
-- Ele organiza os dados das colunas indexadas em uma árvore (B-tree por padrão),
-- permitindo localizar as linhas correspondentes sem varrer a tabela inteira.
-- O índice composto (status, created_at) cobre as duas colunas do WHERE,
-- e como created_at já está ordenado no índice, o ORDER BY não exige etapa extra.
CREATE INDEX idx_processos ON processos(status, created_at);

SELECT * FROM processos
WHERE status = 'ativo'
AND created_at > '2024-01-01'
ORDER BY created_at DESC;
