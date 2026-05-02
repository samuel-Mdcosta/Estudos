//criacao do objeto User e UserPayload para tipagem dos dados do usuario

export interface User {
  id: number;
  name: string;
  email: string;
  avatarUrl: string;
}

//omitindo o id do User para criar o UserPayload, pois o id é gerado automaticamente pelo backend
export type UserPayload = Omit<User, 'id'>;