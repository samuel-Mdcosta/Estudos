"""
Você recebeu um arquivo clientes.json na pasta /data.
O arquivo contém uma lista de objetos com os campos nome, cpf, ativo e saldo.
Escreva uma função que leia esse arquivo e retorne apenas os clientes que estão ativos e com saldo maior que zero, ordenados pelo saldo de forma decrescente.
"""
import json

def lerArquivo(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        clientes = json.load(arquivo)

    ativos_com_saldo = [c for c in clientes if c["ativo"] and c["saldo"] > 0]
    return sorted(ativos_com_saldo, key=lambda c: c["saldo"], reverse=True)
