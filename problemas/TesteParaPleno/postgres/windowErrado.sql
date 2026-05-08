--codigo errado
SELECT
  usuario_id,
  valor,
  SUM(valor) OVER () as total_geral
FROM pedidos
WHERE status = 'pago';

--codigo certo
SELECT 
    usuario_id,
    valor, 
    SUM(valor) OVER(PARTITION BY usuario_id) AS total_por_usuario
    FROM pedidos
    WHERE status = 'pago';

-- o over nao contia uma particiao, assum ele somava todos os valores de todos o susuarios
-- o partition by faz com que a soma seja de um usuario so, a soma vai ser so do 1 e nao do 1 e 2