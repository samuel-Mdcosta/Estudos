//codigo errado
<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  setInterval(() => {
    console.log('rodando...')
  }, 1000)
})
</script>

//codigo certo
<script setup>
import { onMounted, onUnmounted } from 'vue'

onMounted(() => {
  const interval = setInterval(() => {
    console.log('rodando...')
  }, 1000)

  onUnmounted(() => {
    clearInterval(interval)
  })
})


#um memory leak e um vazamento de memoria, onde mesmo depois de um componente ser destruido sua instancia ainda fica na memoria ram
#para evitar esse consumo deve limpara os resursos alocados. tudo que e criado com onMounted deve ser limpo com onUnmounted
#por isso e colocado o clear interval que mesmo depois de ter carregdo a instancia do cronometro fiva na memoria
#depois do onUnmouted e depois do domponentem ser destruido o clearInterval limpa a memoria ram