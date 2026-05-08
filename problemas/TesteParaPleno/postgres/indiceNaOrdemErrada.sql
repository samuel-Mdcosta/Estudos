--codigo errado
SELECT * FROM documentos
WHERE usuario_id = $1
AND tipo = $2
AND created_at > $3;

CREATE INDEX idx_docs ON documentos(created_at, tipo, usuario_id);

--codigo certo
CREATE INDEX idx_docs ON documentos(usuario_id, tipo, created_at);

SELECT * FROM documentos
WHERE usuario_id = $1
AND tipo = $2
AND created_at > $3;


-- --- POR QUE O ÍNDICE ERRADO NÃO AJUDA? ---
--
-- Um índice é como um catálogo telefônico: só é útil se você começa a busca
-- pela primeira coluna da ordenação.
--
-- O índice errado começa por created_at, que é um filtro de intervalo (created_at > $3).
-- O Postgres não consegue pular para um ponto exato num intervalo,
-- ele precisa varrer todas as datas a partir dali sem poder filtrar por usuario_id antes.
-- O índice praticamente não é aproveitado.


-- --- POR QUE A ORDEM CERTA RESOLVE? ---
--
-- A regra é: colunas de igualdade (=) primeiro, colunas de intervalo (>, <, BETWEEN) por último.
--
-- Com (usuario_id, tipo, created_at), o Postgres:
-- 1. Pula direto para o usuario_id exato
-- 2. Dentro desse grupo, filtra pelo tipo exato
-- 3. Só então aplica o filtro de intervalo em created_at
--
-- Isso elimina a grande maioria das linhas antes de chegar no range,
-- tornando a query muito mais rápida.
--
-- Obs: a ordem de criação do índice em relação ao SELECT não importa.
-- O Postgres encontra e usa o índice automaticamente em toda execução da query.