"""
Você recebeu um arquivo processos.csv na pasta /data com 50 mil linhas.
Cada linha contém numero_processo, data_entrada, status e valor_causa.
Escreva uma função que leia esse arquivo sem carregar tudo na memória e retorne apenas os processos com status "ativo" e valor da causa acima de R$10.000,00.
"""
import csv

def ler_csv(caminho):
    processos = []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            if linha["status"] == "ativo" and float(linha["valor_causa"]) > 10000:
                processos.append(linha)
    return processos
