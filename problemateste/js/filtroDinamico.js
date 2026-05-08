//Você tem um array de objetos em memória representando processos jurídicos, cada um com id, numero, status e parte.
//Crie uma página HTML com um campo de busca que filtre os processos em tempo real conforme o usuário digita
//exibindo os resultados numa lista abaixo do campo.

const processos = [
  { id: 1, numero: "0001/2024", status: "ativo", parte: "João Silva" },
  { id: 2, numero: "0002/2024", status: "arquivado", parte: "Maria Souza" }
]

function renderizar(lista) {
    const ul = document.getElementById("lista")
    ul.innerHTML = ""
    lista.forEach(p => {
        const li = document.createElement("li")
        li.textContent = `${p.numero} — ${p.parte} (${p.status})`
        ul.appendChild(li)
    });
}

document.getElementById("busca").addEventListener("input", function (){
    const termo = this.value.toLowerCase()
    const filtrados = processos.filter(p =>
        p.numero.toLowerCase().includes(termo) ||
        p.parte.toLowerCase().includes(termo) ||
        p.status.toLowerCase().includes(termo)
    )
    renderizar(filtrados)
})

renderizar(processos)
