"""
Dada uma lista de inteiros e um número k, encontre a soma máxima de qualquer subarray
contíguo de tamanho k. Implemente em O(n) — sem recalcular a soma do zero a cada posição.
Depois generalize para encontrar o subarray de tamanho variável — entre min_k e max_k —
cuja média é a maior possível.
Exemplo: [2, 1, 5, 1, 3, 2], k=3 → 9 (subarray [5,1,3])
"""


# --- Parte 1: janela fixa de tamanho k, soma máxima ---
#
# Ideia: calcula a soma da primeira janela uma vez.
# A cada passo, desliza a janela somando o novo elemento
# e subtraindo o que saiu — O(n) sem recalcular do zero.
#
# [2, 1, 5, 1, 3, 2]  k=3
#  └──┘        soma = 8
#     └──┘     soma = 7  (+5 -2)
#        └──┘  soma = 9  (+1 -1) ← máximo
#           └──┘ soma = 6  (+3 -5)

def soma_maxima(nums, k):
    soma_atual = sum(nums[:k])
    soma_max   = soma_atual

    for i in range(k, len(nums)):
        soma_atual += nums[i] - nums[i - k]  # entra nums[i], sai nums[i-k]
        soma_max = max(soma_max, soma_atual)

    return soma_max


# --- Parte 2: janela variável entre min_k e max_k, maior média ---
#
# Ideia: para cada posição final j, testa todos os tamanhos válidos
# (de min_k até max_k) usando prefix_sum para calcular qualquer
# soma em O(1) → total O(n * (max_k - min_k)), aceitável na prática.
#
# prefix_sum[i] = soma de nums[0..i-1]
# soma de nums[l..r] = prefix_sum[r+1] - prefix_sum[l]

def media_maxima(nums, min_k, max_k):
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    melhor_media  = float("-inf")
    melhor_inicio = 0
    melhor_fim    = min_k - 1

    for fim in range(min_k - 1, n):
        inicio_min = fim - max_k + 1
        inicio_max = fim - min_k + 1

        for inicio in range(max(0, inicio_min), inicio_max + 1):
            tamanho = fim - inicio + 1
            soma    = prefix[fim + 1] - prefix[inicio]
            media   = soma / tamanho

            if media > melhor_media:
                melhor_media  = media
                melhor_inicio = inicio
                melhor_fim    = fim

    return {
        "subarray": nums[melhor_inicio: melhor_fim + 1],
        "media":    round(melhor_media, 4),
        "indices":  (melhor_inicio, melhor_fim),
    }


# --- testes ---
nums = [2, 1, 5, 1, 3, 2]

print("=== Parte 1 — soma máxima janela fixa ===")
print(f"soma_maxima({nums}, k=3) →", soma_maxima(nums, k=3))   # esperado: 9

print("\n=== Parte 2 — maior média janela variável ===")
print(f"media_maxima({nums}, min_k=2, max_k=4) →", media_maxima(nums, min_k=2, max_k=4))
