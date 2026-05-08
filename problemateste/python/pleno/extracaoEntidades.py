"""
Você recebe uma string com o texto completo de uma petição jurídica. Escreva uma função que extraia
e retorne um dicionário estruturado com: todos os CPFs encontrados com validação de dígito verificador,
todos os CNPJs encontrados, todas as datas no formato DD/MM/AAAA, o número do processo no padrão CNJ
NNNNNNN-DD.AAAA.J.TT.OOOO, e o valor da causa no formato R$ X.XXX,XX.
Use apenas regex e bibliotecas padrão do Python.
"""
import re


def validar_cpf(cpf):
    cpf = re.sub(r"\D", "", cpf)
    #bloqueia cpfs com sequencia de numeros ou menores de 11
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False

    #verifica os dois ultimos digitos o 
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    dig1 = (soma * 10 % 11) % 10
    if dig1 != int(cpf[9]):
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    dig2 = (soma * 10 % 11) % 10
    return dig2 == int(cpf[10])


def extrair_entidades(texto):
    cpfs_encontrados = re.findall(r"\d{3}\.\d{3}\.\d{3}-\d{2}", texto)
    cpfs_validos = [cpf for cpf in cpfs_encontrados if validar_cpf(cpf)]

    cnpjs = re.findall(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", texto)

    datas = re.findall(r"\b\d{2}/\d{2}/\d{4}\b", texto)

    processo = re.search(r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", texto)

    valor = re.search(r"R\$\s*[\d.]+,\d{2}", texto)

    return {
        "cpfs":      cpfs_validos,
        "cnpjs":     cnpjs,
        "datas":     datas,
        "processo":  processo.group() if processo else None,
        "valor_causa": valor.group() if valor else None,
    }


texto = """
Excelentíssimo Juiz,

Processo nº 0001234-56.2024.8.26.0100, distribuído em 10/03/2024.

Requerente: João Silva, CPF 123.456.789-09, nascido em 01/01/1980.
Empresa Ré: Acme Ltda, CNPJ 12.345.678/0001-95.

Valor da causa: R$ 15.000,00.

Advogado: Maria Souza, CPF 111.111.111-11 (inválido).
"""

resultado = extrair_entidades(texto)
for chave, valor in resultado.items():
    print(f"{chave}: {valor}")
