//esse script e responsavel por criar a store de usuario usando o Pinia, que e uma biblioteca de gerenciamento de estado para Vue.js
//esse gerenciamento e armazenamento global o que faz com que os dados do usuario possam ser acessados e modificados de qualquer componente da aplicacao
//assim caso o componente a modifique o nome do usuario o B renderiza acessando o aramzenamento global de estado e exibindo o nome atualizado do usuario
import { defineStore } from 'pinia';
import { ref, type Ref } from 'vue';
import { userService } from '@/services/userService';
import type { User, UserPayload } from '@/types/user';

//definindo a store de usuario usando o defineStore do Pinia, que recebe um nome unico para a store e uma funcao que retorna os estados, actions e getters da store
export const useUserStore = defineStore('user', () => {
    //definindo o estado da store, que e um array de usuarios do tipo User
    const users: Ref<User[]> = ref([]);
    //definindo o estado de loading para indicar se a requisicao de dados do usuario esta em andamento
    const loading: Ref<boolean> = ref(false);
    //definindo o estado de error para armazenar mensagens de erro caso a requisicao de dados do usuario falhe
    const error: Ref<string | null> = ref(null);

    const fetchUsers = async () => {
        //definindo o estado de loading como true para indicar que a requisicao de dados do usuario esta em andamento
        loading.value = true;
        //definindo o estado de error como null para limpar mensagens de erro anteriores
        error.value = null;
        try {
            //chamando a funcao getUsers do userService para puxar a lista de usuarios do backend e armazenando o resultado no estado de users
            users.value = await userService.getUsers();
        } catch (err) {
            //caso a requisicao de dados do usuario falhe, definindo o estado de error com a mensagem de erro
            error.value = (err as Error).message;
        } finally {
            //definindo o estado de loading como false para indicar que a requisicao de dados do usuario terminou, seja com sucesso ou com erro
            loading.value = false;
        }
    }

    const createUser = async (payload: UserPayload) => {
      //chamando a funcao createUser do userService para criar um novo usuario no backend com os dados do payload e armazenando o resultado no estado de users, adicionando o novo usuario ao array de usuarios existente
      const newUser = await userService.createUser(payload)
      users.value.push(newUser)
    }


    const deleteUser = async (id: number) => {
        //chamando a funcao deleteUser do userService para deletar um usuario existente no backend com o id do usuario e atualizando o estado de users, removendo o usuario deletado do array de usuarios existente
      await userService.deleteUser(id)
      users.value = users.value.filter(u => u.id !== id)
    }

    //retornando os estados, actions e getters da store para que possam ser acessados e modificados por outros componentes da aplicacao
    return { users, loading, error, fetchUsers, createUser, deleteUser };
});




