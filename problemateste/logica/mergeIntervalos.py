def merge(intervalos: list[list[int]]) -> list[list[int]]:
    if not intervalos:
        return []

    ordenados = sorted(intervalos, key=lambda iv: iv[0])
    resultado = [ordenados[0][:]]  # cópia para não mutar o input

    for inicio, fim in ordenados[1:]:
        ultimo = resultado[-1]
        if inicio <= ultimo[1]:          # sobrepõe ou toca: expande se necessário
            ultimo[1] = max(ultimo[1], fim)
        else:
            resultado.append([inicio, fim])

    return resultado


def intersecao(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    """
    Retorna os intervalos que pertencem a ambos os conjuntos.
    Usa dois ponteiros que avançam pelo intervalo que termina primeiro.
    """
    resultado = []
    i = j = 0

    while i < len(a) and j < len(b):
        ini = max(a[i][0], b[j][0])
        fim = min(a[i][1], b[j][1])

        if ini <= fim:
            resultado.append([ini, fim])

        # avança o intervalo que termina primeiro
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1

    return resultado


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # --- merge ---
    assert merge([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
    assert merge([[1,4],[4,5]])                == [[1,5]]   # intervalos que se tocam
    assert merge([[1,4],[2,3]])                == [[1,4]]   # contido dentro de outro
    assert merge([[1,2],[3,4],[5,6]])           == [[1,2],[3,4],[5,6]]  # sem sobreposicao
    assert merge([[6,8],[1,9],[2,4]])           == [[1,9]]  # entrada fora de ordem
    assert merge([])                           == []
    assert merge([[1,5]])                      == [[1,5]]

    # --- intersecao ---
    # Caso basico: A=[1-3, 5-9] , B=[2-4, 6-8, 10-15]
    a = [[1,3],[5,9]]
    b = [[2,4],[6,8],[10,15]]
    assert intersecao(a, b) == [[2,3],[6,8]]

    # Sem nenhuma intersecao
    assert intersecao([[1,2]], [[3,4]])   == []

    # Todos se sobrepoem totalmente
    assert intersecao([[1,10]], [[2,5],[6,9]]) == [[2,5],[6,9]]

    # Intervalos identicos
    assert intersecao([[1,5],[7,10]], [[1,5],[7,10]]) == [[1,5],[7,10]]

    # Um conjunto vazio
    assert intersecao([], [[1,2]]) == []

    print("Todos os testes passaram.")

    # Demonstracao
    ex = [[1,3],[2,6],[8,10],[15,18]]
    print(f"\nmerge{ex}")
    print(f"  -> {merge(ex)}")

    a = [[1,3],[5,9]]
    b = [[2,4],[6,8],[10,15]]
    print(f"\nintersecao({a},")
    print(f"           {b})")
    print(f"  -> {intersecao(a, b)}")
