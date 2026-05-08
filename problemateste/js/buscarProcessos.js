//Crie uma página HTML com um botão "Buscar Processos".
//Ao clicar, a página deve fazer uma requisição GET para https://api.exemplo.com/processos
//exibir os resultados numa tabela com as colunas numero, status e valor, e mostrar uma mensagem de erro amigável caso a requisição falhe.




<button id="btn-buscar"></button>

document.getElementById("btn-buscar").addEventListener("click", buscarProcessos);

async function buscarProcessos() {
  const erro = document.getElementById("erro");
  const tabela = document.getElementById("tabela");
  const corpo = document.getElementById("corpo-tabela");

  erro.textContent = "";
  tabela.style.display = "none";
  corpo.innerHTML = "";

  try {
    const resposta = await fetch("https://api.exemplo.com/processos");

    if (!resposta.ok) {
      throw new Error();
    }

    const processos = await resposta.json();

    processos.forEach(processo => {
      const linha = document.createElement("tr");
      linha.innerHTML = `
        <td>${processo.numero}</td>
        <td>${processo.status}</td>
        <td>${processo.valor}</td>
      `;
      corpo.appendChild(linha);
    });

    tabela.style.display = "table";

  } catch {
    erro.textContent = "Não foi possível carregar os processos. Tente novamente mais tarde.";
  }
}


