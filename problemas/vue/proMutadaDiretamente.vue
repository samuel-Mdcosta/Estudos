//codigo errado
<script setup>
const props = defineProps(['usuario'])

function salvar() {
  props.usuario.nome = 'Novo Nome' // problema aqui
}
</script>

//codigo certo
<script setup>
const props = defineProps(['usuario'])

function salvar(){
    emit('salvarUsuario', {props.usuario.nome = 'Novo Nome'})
}

#uma prop nao pode mudar diretamente pois o vue e reativo
#para mudar o valor de uma prop deve avisar o pai que o valor dela foi alterado
#para isso udamos o emit, que emite um evento para o pai