"""
Escreva um decorator @retry que ao ser aplicado numa função, execute-a automaticamente novamente
caso ela lance uma exceção. O decorator deve aceitar os parâmetros max_tentativas e espera_segundos.
A cada nova tentativa o tempo de espera deve dobrar — backoff exponencial. Se todas as tentativas
falharem, deve relançar a última exceção com um log indicando quantas tentativas foram feitas.
Aplique o decorator numa função que simula uma chamada instável a uma API externa.
"""
import time
import random
import logging
import functools

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def retry(max_tentativas=3, espera_segundos=1):
    # retry é um "decorator factory": uma função que recebe configuração
    # e devolve o decorator real. Isso permite usar @retry(max_tentativas=4).
    def decorador(func):
        @functools.wraps(func)  # preserva __name__, __doc__ etc. da função original
        def wrapper(*args, **kwargs):
            espera = espera_segundos  # cópia local — vai dobrar a cada falha

            for tentativa in range(1, max_tentativas + 1):
                try:
                    return func(*args, **kwargs)  # executa a função decorada
                except Exception as e:
                    logging.warning(f"Tentativa {tentativa}/{max_tentativas} falhou: {e}")

                    if tentativa == max_tentativas:
                        # Esgotou todas as tentativas: relança a última exceção
                        # sem engolir o traceback original (bare raise).
                        logging.error(f"Todas as {max_tentativas} tentativas falharam.")
                        raise

                    time.sleep(espera)  # aguarda antes de tentar de novo
                    espera *= 2         # backoff exponencial: 1s → 2s → 4s → 8s ...

        return wrapper
    return decorador


# Simula uma chamada a uma API externa que falha 75% das vezes.
# Com max_tentativas=4 e espera_segundos=1, as pausas entre tentativas
# serão: 1s, 2s, 4s (só ocorrem se houver falha antes da última tentativa).
@retry(max_tentativas=4, espera_segundos=1)
def chamar_api():
    if random.random() < 0.75:  # 75% de chance de falhar
        raise ConnectionError("API instável: sem resposta.")
    return {"status": "ok", "dados": "resultado da API"}


resultado = chamar_api()
print("Sucesso:", resultado)
