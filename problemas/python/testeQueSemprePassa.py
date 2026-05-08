#codigo errado
def test_buscar_documento():
    resultado = buscar_documento(id=999)
    assert resultado is not None or resultado is None

#codigo certo
def test_buscar_documento():
    resultado = buscar_docuento(id=999)
    assert resultado is not None
    assert resultado["id"] == 999

#o assert e uma funcao que valida a veracidade do argumento
# o problema e que o or faz sempre passar no teste 
# o or faz com que uma das condicoes sempre seja true por isso passa no teste
