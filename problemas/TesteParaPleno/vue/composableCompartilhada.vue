//codigo errado // useDocumento.js const documento = ref(null) // fora da função
export function useDocumento() { return { documento } } //codigo certo export
function useDocumentos(){ const documento = ref(null) return {documento} } //
--- POR QUE O CÓDIGO ERRADO É PROBLEMÁTICO? --- // // Imagine que você tem um
bloco de notas na mesa da sala. // Qualquer pessoa da casa que precisar anotar
algo pega o MESMO bloco. // Se João escreve "comprar leite" e Maria abre o
bloco, ela vê a anotação do João. // // É exatamente isso que acontece com o ref
fora da função: // arquivos JavaScript são carregados uma única vez pelo
navegador. // O documento é criado uma vez e todos os componentes que chamam
useDocumento() // recebem o mesmo objeto. Um componente alterando o documento
afeta todos os outros. // --- POR QUE A SOLUÇÃO RESOLVE? --- // // Mover o ref
para dentro da função é como dar um bloco de notas novo // para cada pessoa que
pedir um. João tem o dele, Maria tem o dela. // O que um escreve não aparece no
do outro. // // Toda vez que um componente chama useDocumento(), a função
executa do zero // e cria um ref novo e independente. O estado fica isolado por
componente. // // Exceção: se você QUISER estado global de verdade (ex: usuário
logado, carrinho de compras), // aí faz sentido deixar o ref fora da função de
propósito. // Mas para dados de um componente específico, sempre dentro.
