#codigo errado
modelo.fit(X, y)
score = modelo.score(X, y)
print(f"Acurácia: {score}")

#codigo certo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
modelo.fit(X_train, y_train)
score = modelo.score(X_test, y_test)
print(f"Acurácia: {score:.2f}")

# POR QUE E UM PROBLEMA:
# modelo.score(X, y) avalia o modelo nos mesmos dados usados no treinamento.
# O modelo ja viu esses dados durante o fit, entao ele tende a acertar muito —
# nao porque aprendeu o padrao, mas porque memorizou os exemplos.
# O score fica artificialmente alto e nao representa o comportamento real
# do modelo diante de dados novos. Isso e chamado de data leakage na avaliacao.

# POR QUE A SOLUCAO FUNCIONA:
# train_test_split separa os dados antes do treinamento — 80% para treino e 20% para teste.
# O modelo aprende apenas com X_train e y_train, e nunca ve X_test durante o fit.
# Quando modelo.score(X_test, y_test) e chamado, o modelo esta sendo avaliado
# em dados genuinamente novos, entao o score reflete a capacidade real de generalizacao.
