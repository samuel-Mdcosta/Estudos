"""
Implemente busca binária que encontre um elemento numa lista ordenada em O(log n).
Depois generalize para:
- encontrar a primeira ocorrência de um elemento repetido
- encontrar a última ocorrência
- encontrar o menor elemento numa lista rotacionada ex: [4,5,6,7,0,1,2]
Explique a complexidade de cada variação.
"""


# --- 1. Busca binária clássica — O(log n) ---
#
# A cada iteração descarta metade da lista comparando com o meio.
# n=8 → 3 passos | n=1.000.000 → 20 passos
#
def busca_binaria(nums, alvo):
    esq, dir = 0, len(nums) - 1
    while esq <= dir:
        # // é divisão inteira: descarta a parte decimal e retorna sempre um int.
        # Necessário aqui porque índice de lista não pode ser float.
        # Exemplo: (0 + 6) // 2 = 3   |   (3 + 6) // 2 = 4   (não 4.5)
        meio = (esq + dir) // 2
        if nums[meio] == alvo:
            return meio
        elif nums[meio] < alvo:
            esq = meio + 1
        else:
            dir = meio - 1
    return -1


# --- 2. Primeira ocorrência — O(log n) ---
#
# Quando encontra o alvo NÃO para: guarda o índice e continua
# buscando à ESQUERDA para ver se há uma ocorrência anterior.
#
def primeira_ocorrencia(nums, alvo):
    esq, dir = 0, len(nums) - 1
    resultado = -1
    while esq <= dir:
        meio = (esq + dir) // 2
        if nums[meio] == alvo:
            resultado = meio
            dir = meio - 1  # continua buscando à esquerda
        elif nums[meio] < alvo:
            esq = meio + 1
        else:
            dir = meio - 1
    return resultado


# --- 3. Última ocorrência — O(log n) ---
#
# Mesmo princípio: quando encontra o alvo continua buscando
# à DIREITA para ver se há uma ocorrência posterior.
#
def ultima_ocorrencia(nums, alvo):
    esq, dir = 0, len(nums) - 1
    resultado = -1
    while esq <= dir:
        meio = (esq + dir) // 2
        if nums[meio] == alvo:
            resultado = meio
            esq = meio + 1  # continua buscando à direita
        elif nums[meio] < alvo:
            esq = meio + 1
        else:
            dir = meio - 1
    return resultado


# --- 4. Menor elemento em lista rotacionada — O(log n) ---
#
# [4, 5, 6, 7, 0, 1, 2]  ← rotacionada 4 posições
#
# Invariante: o menor está no ponto de "queda" (onde nums[i] > nums[i+1]).
# Se nums[meio] > nums[dir], a queda está à DIREITA → esq = meio + 1
# Senão a queda está à ESQUERDA ou meio é o menor → dir = meio
#
#  esq=0 dir=6  meio=3  nums[3]=7 > nums[6]=2  → esq=4
#  esq=4 dir=6  meio=5  nums[5]=1 < nums[6]=2  → dir=5
#  esq=4 dir=5  meio=4  nums[4]=0 < nums[5]=1  → dir=4
#  esq=4 dir=4  → retorna nums[4] = 0  ✓
#
def menor_rotacionado(nums):
    esq, dir = 0, len(nums) - 1
    while esq < dir:
        meio = (esq + dir) // 2
        if nums[meio] > nums[dir]:
            esq = meio + 1
        else:
            dir = meio
    return nums[esq]


# --- testes ---
print("=== 1. Busca clássica ===")
print(busca_binaria([1, 3, 5, 7, 9, 11], 7))    # → 3

print("\n=== 2. Primeira ocorrência ===")
print(primeira_ocorrencia([1, 2, 2, 2, 3, 4], 2))  # → 1

print("\n=== 3. Última ocorrência ===")
print(ultima_ocorrencia([1, 2, 2, 2, 3, 4], 2))    # → 3

print("\n=== 4. Menor em lista rotacionada ===")
print(menor_rotacionado([4, 5, 6, 7, 0, 1, 2]))    # → 0
print(menor_rotacionado([3, 4, 5, 1, 2]))           # → 1
print(menor_rotacionado([1, 2, 3, 4, 5]))           # → 1 (sem rotação)