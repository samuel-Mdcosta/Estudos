from dataclasses import dataclass

MATCHING = {')': '(', ']': '[', '}': '{'}
OPENERS  = set(MATCHING.values())


def is_balanced(s: str) -> bool:
    stack = []
    for ch in s:
        if ch in OPENERS:
            stack.append(ch)
        elif stack and stack[-1] == MATCHING[ch]:
            stack.pop()
        else:
            return False
    return not stack


# ---------------------------------------------------------------------------

@dataclass
class Mismatch:
    char: str
    position: int

    def __str__(self) -> str:
        return f"'{self.char}' na posicao {self.position}"


def check_balanced(s: str) -> tuple[bool, Mismatch | None]:
    """
    Retorna (True, None) se balanceado.
    Retorna (False, Mismatch) indicando o caractere e posição do problema.

    Dois casos de desbalanceamento:
      1. Fechador sem abridor correspondente (ex: "([)]" — ')' fecha sobre '[').
      2. Abridor nunca fechado — reporta o mais interno (topo da pilha).
    """
    stack: list[tuple[str, int]] = []  # (char, index)

    for i, ch in enumerate(s):
        if ch in OPENERS:
            stack.append((ch, i))
        else:
            if not stack or stack[-1][0] != MATCHING[ch]:
                return False, Mismatch(ch, i)
            stack.pop()

    if stack:
        char, pos = stack[-1]  # abridor mais interno sem fechador
        return False, Mismatch(char, pos)

    return True, None


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- is_balanced ---
    assert is_balanced("()[]{}")  is True
    assert is_balanced("{[]}")    is True
    assert is_balanced("([)]")    is False
    assert is_balanced("(")       is False
    assert is_balanced("")        is True

    # --- check_balanced ---
    ok, err = check_balanced("()[]{}")
    assert ok and err is None

    ok, err = check_balanced("{[]}")
    assert ok and err is None

    # fechador incorreto: ')' na pos 2 fecha sobre '['
    ok, err = check_balanced("([)]")
    assert not ok and err == Mismatch(')', 2)

    # abridor sem fechador: '(' na pos 0
    ok, err = check_balanced("(")
    assert not ok and err == Mismatch('(', 0)

    # abridor mais interno sem fechar: '[' na pos 1
    ok, err = check_balanced("([")
    assert not ok and err == Mismatch('[', 1)

    # fechador sem nenhum abridor
    ok, err = check_balanced(")")
    assert not ok and err == Mismatch(')', 0)

    # aninhamento profundo correto
    ok, err = check_balanced("{[()]}")
    assert ok and err is None

    print("Todos os testes passaram.")
    print()

    casos = ["()[]{}", "([)]", "{[]}", "(", "([", ")", "{[()}"]
    for s in casos:
        ok, err = check_balanced(s)
        status = "OK" if ok else f"ERRO: {err}"
        print(f"  {s!r:15} -> {status}")
