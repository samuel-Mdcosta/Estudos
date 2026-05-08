"""
Escreva uma função que receba o texto bruto extraído de um PDF jurídico e retorne o texto limpo
sem linhas em branco consecutivas, sem espaços duplos, sem caracteres especiais que não sejam letras, números, vírgulas, pontos e parênteses, e com todas as palavras com a primeira letra maiúscula.
"""
import re

def limpar_texto(texto):
    texto = re.sub(r"[^\w\s,.()\n]", "", texto)

    texto = re.sub(r" {2,}", " ", texto)

    texto = re.sub(r"\n{2,}", "\n", texto)

    texto = texto.title()

    return texto.strip()


texto_bruto = """
CONTRATO  de  prestação!!   de serviços...

   parte contratante: João Silva -- CPF: 123.456.789-00

   valor  da causa: R$ 15.000,00 (quinze mil reais)


   termos e condições @@ aceitos pelas #partes.
"""

print(limpar_texto(texto_bruto))
