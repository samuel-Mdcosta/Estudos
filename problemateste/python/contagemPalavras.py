""" 
Você tem uma string com o texto extraído de um documento jurídico.
Escreva uma função que receba essa string e retorne um dicionário com as 10 palavras mais frequentes.
ignorando palavras com menos de 4 letras e desconsiderando maiúsculas e minúsculas.
"""

string = "O contrato foi assinado após longa negociação entre as partes envolvidas. O contrato estabelecia cláusulas sobre responsabilidade e indenização. A negociação durou semanas. A responsabilidade de cada parte foi definida claramente. O prazo de indenização foi estipulado. O tribunal analisou o documento com atenção. A decisão do tribunal foi favorável. A cláusula principal protegia ambos os lados. Cada cláusula foi revisada pelo advogado. A sentença encerrou o processo. A sentença trouxe alívio."

def contagemPalavras(string):
    texto = string.lower()
    palavras = texto.split()
    palavras = [p for p in palavras if len(p) >= 4]

    contagem = {}
    for palavra in palavras:
        contagem[palavra] = contagem.get(palavra, 0) + 1
    
    top10 = dict(sorted(contagem.items(), key=lambda x: x[1], reverse=True)[:10])

    return top10

resultado = contagemPalavras(string)

for palavra, quantidade in resultado.items():
    print(f"{palavra}: {quantidade}")
