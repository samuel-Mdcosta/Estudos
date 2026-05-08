def two_sum(nums: list[int], target: int) -> list[int]:
    # complemento → índice onde ele foi visto
    seen: dict[int, int] = {}

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    raise ValueError("Nenhum par encontrado")  # garantido não acontecer pelo enunciado


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    assert two_sum([2, 7, 11, 15], 9)   == [0, 1]
    assert two_sum([3, 2, 4], 6)        == [1, 2]
    assert two_sum([3, 3], 6)           == [0, 1]
    assert two_sum([1, 5, 3, 7], 8)     == [1, 2]  # 5 + 3 = 8
    assert two_sum([-1, -2, -3, -4], -6) == [1, 3] # negativos

    print("Todos os testes passaram.")

    # ---------------------------------------------------------------------------
    # Modo interativo
    # ---------------------------------------------------------------------------
    raw = input("\nArray (ex: 2 7 11 15): ")
    nums = list(map(int, raw.split()))
    target = int(input("Target: "))

    result = two_sum(nums, target)
    print(f"Posições: {result}  →  valores: {nums[result[0]]} + {nums[result[1]]} = {target}")
