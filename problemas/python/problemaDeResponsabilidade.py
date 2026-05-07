#codigo errado
def processar_documento(arquivo):
    # lê o arquivo
    with open(arquivo) as f:
        texto = f.read()
    # limpa o texto
    texto = texto.lower().strip()
    # salva no banco
    db.inserir({"texto": texto})
    # envia email de confirmação
    email.enviar("doc processado")
    return texto

#codigo certo
def processar_documento(arquivo):
    with open(arquivo) as f:
        texto = f.read()
    texto = texto.lower().strip()
    return texto

# POR QUE E UM PROBLEMA:
# A funcao processar_documento viola o principio da responsabilidade unica (SRP).
# Ela faz quatro coisas distintas: le arquivo, limpa texto, salva no banco e envia email.
# Isso torna o codigo dificil de testar — para testar a limpeza do texto voce e obrigado
# a simular banco e email. Alem disso, qualquer mudanca em uma dessas etapas
# (ex: trocar o banco, mudar o template do email) obriga a mexer nessa funcao.

# POR QUE A SOLUCAO FUNCIONA:
# A funcao passa a ter uma unica responsabilidade: ler e limpar o texto.
# A insercao no banco pertence ao repository, e o envio de email pertence ao controller
# ou a um service de notificacao. Quem chama processar_documento decide o que fazer
# com o resultado — a funcao nao precisa saber o que acontece depois dela.