//Crie um formulário HTML com os campos nome (obrigatório, mínimo 3 caracteres), cpf (obrigatório, formato válido) e email (obrigatório, formato válido). 
//Ao submeter, valide os campos com JavaScript puro 
//exiba mensagens de erro inline abaixo de cada campo inválido sem recarregar a página.

<form id="form" novalidate>

  <label for="nome">Nome</label>
  <input type="text" id="nome" placeholder="Digite seu nome" />
  <span id="erro-nome"></span>

  <label for="cpf">CPF</label>
  <input type="text" id="cpf" placeholder="000.000.000-00" maxlength="14" />
  <span id="erro-cpf"></span>

  <label for="email">E-mail</label>
  <input type="email" id="email" placeholder="exemplo@email.com" />
  <span id="erro-email"></span>

  <button type="submit">Enviar</button>

</form>

  const form = document.getElementById("form");

  document.getElementById("cpf").addEventListener("input", function () {
    let v = this.value.replace(/\D/g, "").slice(0, 11);
    v = v.replace(/(\d{3})(\d)/, "$1.$2");
    v = v.replace(/(\d{3})(\d)/, "$1.$2");
    v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
    this.value = v;
  });

  function validarCPF(cpf) {
    cpf = cpf.replace(/\D/g, "");
    if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;

    let soma = 0;
    for (let i = 0; i < 9; i++) soma += parseInt(cpf[i]) * (10 - i);
    let dig1 = (soma * 10) % 11;
    if (dig1 >= 10) dig1 = 0;
    if (dig1 !== parseInt(cpf[9])) return false;

    soma = 0;
    for (let i = 0; i < 10; i++) soma += parseInt(cpf[i]) * (11 - i);
    let dig2 = (soma * 10) % 11;
    if (dig2 >= 10) dig2 = 0;
    return dig2 === parseInt(cpf[10]);
  }

  function setErro(campo, mensagem) {
    document.getElementById(campo).classList.toggle("erro", !!mensagem);
    document.getElementById("erro-" + campo).textContent = mensagem;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const nome  = document.getElementById("nome").value.trim();
    const cpf   = document.getElementById("cpf").value.trim();
    const email = document.getElementById("email").value.trim();

    let valido = true;

    if (nome.length < 3) {
      setErro("nome", "Nome obrigatório com mínimo 3 caracteres.");
      valido = false;
    } else {
      setErro("nome", "");
    }

    if (!validarCPF(cpf)) {
      setErro("cpf", "CPF inválido.");
      valido = false;
    } else {
      setErro("cpf", "");
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setErro("email", "E-mail inválido.");
      valido = false;
    } else {
      setErro("email", "");
    }

    if (valido) {
      alert("Formulário enviado com sucesso!");
      form.reset();
    }
  });
