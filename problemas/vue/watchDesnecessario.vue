<!-- codigo errado --!>
<script setup>
import { ref, watch, computed } from 'vue'

const preco = ref(100)
const desconto = ref(0)
const total = ref(100)

watch([preco, desconto], () => {
  total.value = preco.value - desconto.value
})
</script>

<!-- codigo certo -->
<script setup>
import { ref, computed } from "vue";

const preco = ref(100);
const desconto = ref(0);
const total = computed(() => preco.value - desconto.value);
</script>

<!--
  POR QUE watch É ERRADO AQUI:

  1. `total` é um ref separado com estado próprio → pode ficar fora de sincronia
     se alguém fizer `total.value = 999` diretamente (estado inconsistente).

  2. watch é ASSÍNCRONO por padrão: na primeira renderização `total` ainda vale 100
     (o valor inicial hardcoded), não o resultado do cálculo. O watch só dispara
     após a primeira mudança em preco ou desconto.

  3. É código imperativo para algo declarativo: você está descrevendo "quando X muda,
     atualize Y" em vez de declarar "total É sempre preco - desconto".

  POR QUE computed RESOLVE:

  - `computed` é uma dependência derivada, não um estado separado.
    O Vue rastreia automaticamente quais refs são lidas dentro da função
    e recalcula total apenas quando preco ou desconto mudam.

  - É SÍNCRONO: o valor já está correto na primeira renderização, sem estado inicial manual.

  - É cacheado: se preco e desconto não mudaram, acessar total.value múltiplas vezes
    retorna o valor cacheado sem recalcular.

  - Impossível ficar inconsistente: total não tem setter por padrão,
    ninguém pode escrever um valor errado nele.

  REGRA GERAL:
  - Use computed quando o valor DERIVA de outros estados (leitura).
  - Use watch quando precisa de um EFEITO COLATERAL ao mudar (chamada de API, log, DOM manual).
-->
