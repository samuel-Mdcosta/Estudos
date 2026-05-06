#funcao errada
class DocumentoService:
    def buscar(self, id: str):
        doc = self.repo.find_by_id(id)
        if not doc:
            raise HTTPException(status_code=404, detail="Não encontrado")
        return doc
    
#funcao correta
class DocumentoService:
    def buscar(self, id: str):
        doc = self.repo.find_by_id(id)
        if not doc:
            raise DocumentosNaoEncontrados(f"Documentos {id} não encontrado")
        return doc
    
#a camada de service ela deve ser especifica para regra de negocio
#ela nao sabe sobre http, porem ela deveser capaz de lidar com erros, assim ela lanca esse erro para o arquivo handler
#pois cada camada deve saber apenas sobre sua reponsabilidade
#mesmo o service nao sendo responsavel por lidar com execessoe sele deve interromper o fluxo quando algo da errado