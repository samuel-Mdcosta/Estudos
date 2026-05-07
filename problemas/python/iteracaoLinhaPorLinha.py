#codigo errado
for index, row in df.iterrows():
    df.at[index, 'texto_limpo'] = row['texto'].lower().strip()

#codigo certo
df['texto_limpo'] = df['texto'].str.lower().str.strip()

# POR QUE E UM PROBLEMA:
# O iterrows() converte cada linha do DataFrame em um objeto Series do Python a cada iteracao.
# Isso significa que o pandas perde toda a vantagem de trabalhar com arrays contiguos em memoria.
# O df.at[index, ...] faz uma escrita celula por celula, forçando o pandas a localizar
# e modificar cada posicao individualmente. Em DataFrames grandes isso e extremamente lento.

# POR QUE A SOLUCAO FUNCIONA:
# df['texto'].str.lower().str.strip() aplica a transformacao em toda a coluna de uma vez.
# Internamente o pandas percorre o array uma unica vez em C, sem criar objetos Python
# intermediarios por linha. O resultado e atribuido diretamente a coluna 'texto_limpo'
# em uma operacao so — sem loop, sem escrita celula por celula.
