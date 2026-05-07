#codigo errado
<template>
  <div v-for="doc in documentos" v-if="doc.ativo" :key="doc.id">
    {{ doc.nome }}
  </div>
</template>

<!-- codigo certo -->
<template>
  <template v-for="doc in documentos" :key="doc.id">
    <div v-if="doc.ativo">
      {{ doc.nome }}
    </div>
  </template>
</template>

<!--
  ORDEM DE AVALIAÇÃO E POR QUE QUEBRA:

  No Vue 2: v-for tem prioridade maior que v-if.
    → o loop roda PRIMEIRO para TODOS os itens, e só depois v-if filtra.
    → funciona, mas é ineficiente: itera documentos inativos desnecessariamente.

  No Vue 3: v-if tem prioridade maior que v-for. (MUDANÇA DE COMPORTAMENTO)
    → v-if é avaliado ANTES de v-for.
    → nesse momento "doc" ainda não existe (o loop nem começou).
    → resultado: erro em runtime — "doc is not defined".

  POR QUE O CODIGO CERTO FUNCIONA:
    → O <template v-for> cria o loop no elemento pai sem renderizar nenhum nó DOM extra.
    → O v-if fica em um elemento filho separado, então "doc" já existe quando v-if é avaliado.
    → Funciona igual no Vue 2 e Vue 3, sem ambiguidade de prioridade.
    → Bônus: o :key fica no <template> externo, que é a prática recomendada no Vue 3.
-->

