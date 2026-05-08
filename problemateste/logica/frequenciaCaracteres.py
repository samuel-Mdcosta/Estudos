def frequencia(s: str) -> dict[str, int]:
    freq: dict[str, int] = {}
    for ch in s:
        if ch != ' ':
            freq[ch] = freq.get(ch, 0) + 1
    return freq


def eh_anagrama(a: str, b: str) -> bool:
    return frequencia(a.lower()) == frequencia(b.lower())


def primeiro_nao_repetido(s: str) -> str | None:
    freq = frequencia(s)
    for ch in s:
        if ch != ' ' and freq[ch] == 1:
            return ch
    return None


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # --- frequencia ---
    assert frequencia("aabbcde") == {'a': 2, 'b': 2, 'c': 1, 'd': 1, 'e': 1}
    assert frequencia("a b c")   == {'a': 1, 'b': 1, 'c': 1}
    assert frequencia("")        == {}

    # --- eh_anagrama ---
    assert eh_anagrama("listen", "silent")          is True
    assert eh_anagrama("Astronomer", "Moon starer") is True   # case + espacos
    assert eh_anagrama("hello", "world")            is False
    assert eh_anagrama("abc", "ab")                 is False

    # --- primeiro_nao_repetido ---
    assert primeiro_nao_repetido("aabbcde") == 'c'   # a,b repetidos; c e o 1 unico
    assert primeiro_nao_repetido("aabb")    is None
    assert primeiro_nao_repetido("z")       == 'z'
    assert primeiro_nao_repetido("aabbc")   == 'c'
    assert primeiro_nao_repetido("abacaba") == 'c'   # a=4, b=2, c=1; 1 unico: c(pos 3)

    print("Todos os testes passaram.")

    s = "aabbcde"
    print(f"\nstring          : {s!r}")
    print(f"frequencia      : {frequencia(s)}")
    print(f"anagrama 'bbaacde'? {eh_anagrama(s, 'bbaacde')}")
    print(f"1o nao repetido : {primeiro_nao_repetido(s)!r}")
