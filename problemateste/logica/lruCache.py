class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[int, Node] = {}

        # Sentinels: head = LRU end, tail = MRU end
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_before_tail(self, node: Node) -> None:
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_before_tail(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._insert_before_tail(node)
        if len(self.cache) > self.capacity:
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cache = LRUCache(2)

    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1        # acessa 1 → torna-se MRU

    cache.put(3, 3)                 # evict 2 (LRU)
    assert cache.get(2) == -1       # 2 foi removido
    assert cache.get(3) == 3

    cache.put(4, 4)                 # evict 1 (LRU)
    assert cache.get(1) == -1       # 1 foi removido
    assert cache.get(3) == 3
    assert cache.get(4) == 4

    # Atualização de valor existente não deve exceder capacidade
    cache.put(3, 30)
    assert cache.get(3) == 30
    assert len(cache.cache) == 2

    print("Todos os testes passaram.")
