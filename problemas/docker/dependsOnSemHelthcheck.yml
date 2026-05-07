#codigo errado
services:
  api:
    build: .
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15

  redis:
    image: redis:7

#codigo certo
services:
  api:
    build: .
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  postgres:
    image: postgres:15
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 5s
      retries: 5

  redis:
    image: redis:7
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      retries: 5

#codigo errado: depends_on sem condition so espera o container iniciar.
#iniciar nao significa estar pronto para aceitar conexoes.
#o postgres e o redis podem ainda estar subindo quando a api ja tenta conectar.
#isso causa erro de conexao na api na inicializacao.
#
#codigo certo: healthcheck define um comando para testar se o servico esta pronto.
#pg_isready verifica se o postgres esta aceitando conexoes.
#redis-cli ping verifica se o redis esta respondendo.
#condition: service_healthy faz a api esperar o healthcheck passar antes de subir.
