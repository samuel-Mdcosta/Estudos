#codigo errado
def chunkar(texto: str) -> list[str]:
    tamanho = 500
    return 
    [texto[i:i+tamanho] 
     for i in range(0, len(texto), tamanho)]
    
#codigo certo
def chunkar(texto: str, tamanho: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    i = 0
    while i < len(texto):
        chunk = texto[i:i+tamanho]
        chunks.append(chunk)
        i += tamanho - overlap
    return chunks

#o erro de chunks com tamanho fixo e que ele pode conrtar frases que seria muito boas para o cntexto e sdimilaridade no meio
#a tratativa do overlap faz com que o proximo chuncks nao comece da onde o anterior parou, ele comece alguns caracteres antes