//codigo errado
<template>
  <div v-for="(item, index) in lista" :key="index">
    {{ item.nome }}
  </div>
</template>

//codigo certo
<template>
  <div v-for="item in lista" :key="item.id">
    {{ item.nome }}
  </div>
</template>

#o v-for e itilizado para rendertizar uma lista de elementos baseado em array ou
objeto #:key e necessario para performance e estabilidade da renderizacao
#ajudando o vue a identificar quais itens doram adicionasos ou removidos
#utilizar o index na jey faz com que o vue nao consiga identificar quais itens
foram alterados, o que pode levar a bugs e problemas de performance
