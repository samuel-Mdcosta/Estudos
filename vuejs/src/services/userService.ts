import type { User, UserPayload } from "@/types/user";
//nao importa o arquivo e sim a interface e o type para tipagem dos dados do usuario

const API_URL = "http://localhost:3000/users";
//rota que estaria o backend para o recurso de usuarios

export const userService = {
    //puxa a lista de parametros do usuario do backend e retorna um array de usuarios
    async getUsers(): Promise<User[]> {
        //chama a rtoa que esta o obj de usuario
        const response = await fetch(API_URL);
        if (!response.ok) {
            // se nao conseguir puxar os parametros do usuario, retorna um erro
            throw new Error("Failed to fetch users");
        }
        // caso consiga retorna um json com a lista de parametros do objeto
        return response.json();
    }
}

//CREATE
async function createUser(userPayload: UserPayload): Promise<User> {
    //chama a rota do backend para criar um novo usuario, passando os dados do usuario como payload
    const response = await fetch(API_URL, {
        //metodo da rtoa como post
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        //converte o payload do usuario para json e envia no corpo da requisicao
        body: JSON.stringify(userPayload)
    });
    //se nao conseguir criar o usuario, retorna um erro
    if (!response.ok) {
        throw new Error("Failed to create user");
    }
    //caso consiga, retorna o usuario criado como json
    return response.json();
}

//UPDATE
async function updateUser(id: number, userPayload: UserPayload): Promise<User> {
    //chama a rota do backend para atualizar um usuario existente, passando o id do usuario e os dados atualizados como payload
    const response = await fetch(`${API_URL}/${id}`, {
        //metodo da rtoa como put
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        //converte o payload do usuario para json e envia no corpo da requisicao
        body: JSON.stringify(userPayload)
    });
    //se nao conseguir atualizar o usuario, retorna um erro
    if (!response.ok) {
        throw new Error("Failed to update user");
    }
    //caso consiga, retorna o usuario atualizado como json
    return response.json();
}


//REMOVE
async function deleteUser(id: number): Promise<void> {
    //chama a rota do backend para deletar um usuario existente, passando o id do usuario
    const response = await fetch(`${API_URL}/${id}`, {
        //metodo da rtoa como delete
        method: "DELETE"
    });
    //se nao conseguir deletar o usuario, retorna um erro
    if (!response.ok) {
        throw new Error("Failed to delete user");
    }
    //caso consiga, nao retorna nada (void)
}