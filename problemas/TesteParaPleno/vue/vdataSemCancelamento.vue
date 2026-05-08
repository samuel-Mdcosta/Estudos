//codigo errado
<script setup>
async function carregarDados({ page, itemsPerPage }) {
  carregando.value = true;
  const dados = await api.buscar({ page, itemsPerPage });
  itens.value = dados;
  carregando.value = false;
}
</script>

//codigo certo
<script setup>
const abortController = ref(null)

async function carregarDados({ page, itemsPerPage }) {
  if (abortController.value) {
    abortController.value.abort() // cancela a requisição anterior
  }

  abortController.value = new AbortController()

  carregando.value = true
  try {
    const dados = await api.buscar({ page, itemsPerPage }, { signal: abortController.value.signal })
    itens.value = dados
  } catch (e) {
    if (e.name !== 'AbortError') throw e // ignora cancelamentos, relança erros reais
  } finally {
    carregando.value = false
  }
}
</script>


// --- POR QUE O CÓDIGO ERRADO É PROBLEMÁTICO? ---
//
// Imagine que você pede uma pizza de calabresa, mas muda de ideia e pede uma de frango.
// No código errado, as duas pizzas chegam — e a cozinha decide qual você come
// baseada em qual ficou pronta por último, não na sua última escolha.
//
// No v-data-table-server, o usuário pode trocar de página rapidamente:
// página 1, página 2, página 3. Três requisições saem ao mesmo tempo.
// A mais lenta (ex: página 2) pode chegar depois da página 3,
// e o que aparece na tela é a página 2 — que não foi o que o usuário pediu.
// Isso se chama "race condition de requisições" ou resposta fora de ordem.


// --- POR QUE A SOLUÇÃO COM AbortController RESOLVE? ---
//
// AbortController é um sinal de cancelamento nativo do navegador.
// Quando o usuário troca de página, a função dispara um "abort()" na requisição anterior
// antes de iniciar a nova. O navegador cancela a requisição em andamento
// e o catch ignora o erro de cancelamento (AbortError), deixando passar só erros reais.
//
// Assim só a última requisição — a que o usuário realmente quer — chega a atualizar a tela.
// As anteriores são descartadas antes mesmo de processar a resposta.
