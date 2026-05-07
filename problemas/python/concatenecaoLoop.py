#codigo errado
resultado = ""
for chunk in chunks:
    resultado = resultado + chunk
return resultado

#codigo certo
resultado = ""
return resultado.join(chunks)

# Por que o codigo errado é ruim?
# Strings em Python são imutáveis. A cada iteração do loop, Python cria um NOVO objeto string
# copiando todos os caracteres anteriores + o novo chunk.
# Para N chunks de tamanho M, o custo é O(N² * M) em tempo e memória.
#
# Exemplo com 10.000 chunks de 100 caracteres cada:
#   Iteração 1:  copia   100 chars  → novo objeto de   100 chars
#   Iteração 2:  copia   200 chars  → novo objeto de   200 chars
#   Iteração 3:  copia   300 chars  → novo objeto de   300 chars
#   ...
#   Iteração 10000: copia 1.000.000 chars
#   Total de cópias: 100 + 200 + 300 + ... + 1.000.000 = 100 * (1+2+...+10000)
#                  = 100 * (10000 * 10001 / 2) ≈ 5.000.500.000 operações de cópia de char
#   Custo real: ~5 bilhões de operações → lento e usa ~50 GB de memória alocada ao longo do processo
#
# Por que o codigo certo é bom?
# str.join() internamente calcula o tamanho total PRIMEIRO, aloca a memória UMA SÓ VEZ,
# e copia cada chunk diretamente para a posição correta.
# Custo: O(N * M) — linear, não quadrático.
#
# Exemplo com os mesmos 10.000 chunks de 100 caracteres:
#   join aloca 1.000.000 chars de uma vez → faz 10.000 cópias de 100 chars cada
#   Total: 1.000.000 operações de cópia — 5000x mais rápido que o loop