#codigo errado
resposta = llm.invoke(
    prompt,
    temperature=0.9,
    max_tokens=2000
)

#codigo certo
resposta = llm.invoke(
    prompt,
    temperature=0.1,
    max_tokens=2000
)

#o erro e que o calculo da temperatura ela vareia entre 0 a 1, quanto mais proximo de 0 mais a resposta sera menos variada
#e quanto mais perto de 1 mais o modelo alucina e e craitivo na formulacao da resposta