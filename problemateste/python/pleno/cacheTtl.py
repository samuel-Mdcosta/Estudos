import time
import functools
from dataclasses import dataclass
from typing import Any


@dataclass
class _CacheEntry:
    value: Any
    expires_at: float


def cache_ttl(segundos: int = 60):
    """
    Decorator que armazena o retorno de uma função por `segundos`.
    A chave de cache é a combinação exata de (args, kwargs).
    """
    def decorator(func):
        store: dict[tuple, _CacheEntry] = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))

            entry = store.get(key)
            if entry and time.monotonic() < entry.expires_at:
                return entry.value

            result = func(*args, **kwargs)
            store[key] = _CacheEntry(
                value=result,
                expires_at=time.monotonic() + segundos,
            )
            return result

        # Utilitários de inspeção/controle expostos na função decorada
        def cache_clear() -> None:
            store.clear()

        def cache_info() -> dict:
            now = time.monotonic()
            return {
                key: {
                    "value": e.value,
                    "ttl_restante": round(max(0.0, e.expires_at - now), 3),
                }
                for key, e in store.items()
            }

        wrapper.cache_clear = cache_clear
        wrapper.cache_info  = cache_info
        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    call_log: list[str] = []

    @cache_ttl(segundos=1)
    def buscar_documento(id: int) -> str:
        call_log.append(f"executou id={id}")
        return f"doc-{id}"

    # -- Primeira chamada: executa a função
    assert buscar_documento(id=1) == "doc-1"
    assert call_log == ["executou id=1"]

    # -- Segunda chamada mesmos args: usa cache, não executa de novo
    assert buscar_documento(id=1) == "doc-1"
    assert call_log == ["executou id=1"]           # sem nova entrada

    # -- Chave diferente: executa a função separadamente
    assert buscar_documento(id=2) == "doc-2"
    assert call_log == ["executou id=1", "executou id=2"]

    # -- Cache ainda válido para id=1
    assert buscar_documento(id=1) == "doc-1"
    assert len(call_log) == 2

    # -- Aguarda TTL expirar e reexecuta
    time.sleep(1.05)
    assert buscar_documento(id=1) == "doc-1"
    assert call_log == ["executou id=1", "executou id=2", "executou id=1"]

    # -- cache_clear apaga todas as entradas
    buscar_documento(id=3)
    assert any("id=3" in e for e in call_log)
    buscar_documento.cache_clear()
    buscar_documento(id=3)
    assert call_log.count("executou id=3") == 2    # executou de novo após clear

    # -- cache_info mostra entradas vivas
    buscar_documento.cache_clear()
    buscar_documento(id=10)
    info = buscar_documento.cache_info()
    assert len(info) == 1
    key = list(info)[0]
    assert info[key]["value"] == "doc-10"
    assert info[key]["ttl_restante"] <= 1.0

    print("Todos os testes passaram.")
