#um decorator e uma funcao que recebe outra funcao como parametro e retorna uma funcao
#o decorator é usado para adicionar funcionalidades a uma funcao sem modificar o codigo da funcao original
#exemplo: o decorator tem um try catch da rota do banco, e ao inves de voce fazer um novo try catch em cada funcao, voce pode usar o decorator para adicionar essa funcionalidade a todas as funcoes que precisam acessar o banco

def decorator(func):
    # um wrapper é uma funcao que envolve a funcao original e adiciona funcionalidades a ela
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Erro na requisição"}
        except Exception as e:
            return {"error": str(e)}
    return wrapper

@decorator        
def retornaBanco():
    print("Acessando o banco de dados...")
    #simulando uma requisição ao banco de dados
    response = requests.get("http://localhost:8000/banco")
    return response
