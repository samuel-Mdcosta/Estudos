"""
Você recebe uma string com o texto completo de uma petição de 50 páginas.
Escreva uma função que divida esse texto em chunks respeitando as seguintes regras:
- nenhum chunk deve ultrapassar 800 tokens estimados (1 token = 4 caracteres)
- chunks não podem cortar no meio de uma frase — respeite o ponto final
- chunks vizinhos devem ter 10% de sobreposição para manter contexto
- cada chunk deve ser retornado como dicionário com texto, indice, inicio_char e fim_char
"""
import re

MAX_TOKENS    = 800
CHARS_POR_TOKEN = 4
MAX_CHARS     = MAX_TOKENS * CHARS_POR_TOKEN   # 3200 caracteres por chunk
SOBREPOSICAO  = int(MAX_CHARS * 0.10)          # 320 caracteres de overlap


def dividir_em_frases(texto):
    # separa frases pelo ponto final preservando a posição de cada uma
    frases = []
    for match in re.finditer(r"[^.!?]+[.!?]+", texto):
        frases.append((match.group(), match.start(), match.end()))
    return frases


def chunkizar(texto):
    frases = dividir_em_frases(texto)
    chunks = []
    i = 0

    while i < len(frases):
        chunk_texto = ""
        inicio_char = frases[i][1]
        fim_char    = inicio_char
        j = i

        # acumula frases até atingir o limite de caracteres
        while j < len(frases):
            frase, _, fim = frases[j]
            if len(chunk_texto) + len(frase) > MAX_CHARS:
                break
            chunk_texto += frase
            fim_char = fim
            j += 1

        # garante ao menos uma frase por chunk (evita loop infinito)
        if j == i:
            frase, _, fim = frases[i]
            chunk_texto = frase
            fim_char = fim
            j = i + 1

        chunks.append({
            "indice":      len(chunks),
            "texto":       chunk_texto.strip(),
            "inicio_char": inicio_char,
            "fim_char":    fim_char,
        })

        # retrocede o ponteiro para criar sobreposição de 10%
        overlap_acumulado = 0
        i = j - 1
        while i > chunks[-1]["indice"] and overlap_acumulado < SOBREPOSICAO:
            overlap_acumulado += len(frases[i][0])
            i -= 1
        i = max(i, j - 1) if j < len(frases) else j

    return chunks


# --- teste ---
texto_exemplo = (
    "O requerente alega danos morais decorrentes do contrato firmado em 2022. "
    "A parte ré contesta os fatos apresentados na inicial. "
    "O juízo determinou a produção de provas documentais. " * 60
)

chunks = chunkizar(texto_exemplo)

for c in chunks:
    tokens_estimados = len(c["texto"]) // CHARS_POR_TOKEN
    print(f"Chunk {c['indice']} | chars {c['inicio_char']}-{c['fim_char']} | ~{tokens_estimados} tokens")

print(f"\nTotal de chunks: {len(chunks)}")
