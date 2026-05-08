def calcular_digito_cpf(digitos):
    """Calcula o dígito verificador para uma lista de dígitos."""
    soma = 0
    peso = len(digitos) + 1
    
    for digito in digitos:
        soma += int(digito) * peso
        peso -= 1
        
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto

def validar_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, str(cpf)))
    
    if len(cpf) != 11:
        return False
        
    # Cálculo dos dois dígitos
    nove_primeiros = [int(d) for d in cpf[:9]]
    
    dv1 = calcular_digito_cpf(nove_primeiros)
    
    dez_primeiros = nove_primeiros + [dv1]
    dv2 = calcular_digito_cpf(dez_primeiros)
    
    # Verifica se os dígitos calculados coincidem com os originais
    return dv1 == int(cpf[9]) and dv2 == int(cpf[10])

# Exemplo de uso
cpf_teste = "11122233396"
print(f"CPF {cpf_teste} válido? {validar_cpf(cpf_teste)}")
