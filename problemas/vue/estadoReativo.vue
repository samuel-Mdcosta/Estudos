<!-- codigo errado --!>
<script setup>
let contador = 0

function incrementar() {
  contador++
}
</script>

<template>
  <button @click="incrementar">{{ contador }}</button>
</template>

<!-- codigo certo -->
<script setup>
import { ref } from 'vue'

const contador = ref(0)

function incrementar() {
  contador.value++
}
</script>

<template>
  <button @click="incrementar">{{ contador }}</button>
</template>

<!--
  POR QUE O NÚMERO NÃO ATUALIZA NA TELA:

  `let contador = 0` é uma variável JavaScript comum.
  O Vue não tem como saber que ela mudou — ele não "observa" variáveis soltas.
  Quando incrementar() executa `contador++`, o valor interno muda,
  mas o sistema de reatividade do Vue nunca é notificado → o template não re-renderiza.

  POR QUE ref() RESOLVE:
  `ref(0)` retorna um objeto reativo { value: 0 } cujo acesso e escrita
  são interceptados pelo sistema de reatividade do Vue (Proxy interno).
  Quando `contador.value++` é chamado, o Vue detecta a mudança automaticamente
  e agenda um re-render do template.

  No template, `{{ contador }}` (sem .value) funciona porque o Vue
  faz o "unwrap" automático de refs dentro de expressões de template.
-->

