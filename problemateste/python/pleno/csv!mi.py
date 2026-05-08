"""

Você tem um arquivo documentos.csv em /data com 1 milhão de linhas. Cada linha contém id, texto, tipo e data_criacao.
Escreva uma função que processe esse arquivo em lotes de 1000 linhas usando generator, filtre apenas documentos do tipo "peticao" criados nos últimos 90 dias
aplique uma limpeza básica no texto e salve o resultado num novo arquivo peticoes_limpas.csv sem nunca carregar o arquivo inteiro na memória.
"""

import csv
import re
from datetime import datetime, timedelta

def ler_em_lotes(caminho, tamanho_lote=1000):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        lote = []
        for linha in leitor:
            lote.append(linha)
            if len(lote) == tamanho_lote:
                yield lote
                lote = []
        if lote:
            yield lote

def limpar_texto(texto):
    texto = re.sub(r"\s+", " ", texto)
    texto = re.sub(r"[^\w\s,.()\-]", "", texto)
    return texto.strip()

def processar_csv(entrada, saida):
    limite = datetime.now() - timedelta(days=90)
    campos = ["id", "texto", "tipo", "data_criacao"]

    with open(saida, "w", encoding="utf-8", newline="") as arquivo_saida:
        escritor = csv.DictWriter(arquivo_saida, fieldnames=campos)
        escritor.writeheader()

        for lote in ler_em_lotes(entrada):
            for doc in lote:
                if doc["tipo"] != "peticao":
                    continue

                data = datetime.fromisoformat(doc["data_criacao"])
                if data < limite:
                    continue

                doc["texto"] = limpar_texto(doc["texto"])
                escritor.writerow(doc)
