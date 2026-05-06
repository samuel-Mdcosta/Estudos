//codig errado
<script setup>
import { computed } from 'vue'

const dadosFormatados = computed(() => {
  fetch('/api/dados').then(r => r.json()) // problema aqui
  return lista.value.map(x => x.nome)
})
</script>

//codigo certo
<script setup>
import { computed } from 'vue'

const lista = ref([])
const dadosFormatados = computed(() => { lista.value.map(x => x.nome) })

watch(lista, async() =>{
    const response = await fetch('/api/dados')
    lista.value = await response.json()
}, {immediate: true})

#um computed nao pode chamar um api pois ele contem cache, entao ele pode acabar fazendo requisicoes desnecessarias
#ele deve apenas armazenar e formatar os resultados de uma requisicao
#entao para fazer a requisicao usa o watch, que observa quando a requisicao for feita atualiza a lista e o computed atualiza os dados formatados
#a ordem nao altera os fatos nesse caso, pois o computed so vai ser atualizado quando ele for consumido