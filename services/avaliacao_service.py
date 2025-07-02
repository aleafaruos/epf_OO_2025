from bottle import request 
from models.avaliacao import avaliacaoModel, Avaliacao 

class AvaliacaoService: 
    def __init__(self): 
        self.avaliacao_model = avaliacaoModel() 


    def get_all(self): 
        avaliacoes = self.avaliacao_model.get_all() 
        return avaliacoes 


    def save(self): 
        
        id_avaliacao = request.forms.get('id') 
        nota = request.forms.get('nota') 
        nome_usuario = request.forms.get('nome_usuario') 
        comentario = request.forms.get('comentario') 
        id_filme = request.forms.get('id_filme') 
        id_usuario = request.forms.get('id_usuario') 

        
        avaliacao = Avaliacao(
            id=id_avaliacao, 
            nota=nota, 
            nome_usuario=nome_usuario,
            comentario=comentario,
            id_filme=int(id_filme) if id_filme else None, 
            id_usuario=int(id_usuario) if id_usuario else None 
        ) 
        self.avaliacao_model.add_avaliacao(avaliacao) 


    def get_by_id(self, avaliacao_id): 
        return self.avaliacao_model.get_by_id(avaliacao_id) 


    def edit_avaliacao(self, avaliacao): 
       
        avaliacao.nota = request.forms.get('nota') 
        avaliacao.nome_usuario = request.forms.get('nome_usuario') 
        avaliacao.comentario = request.forms.get('comentario') 
        avaliacao.id_filme = int(request.forms.get('id_filme')) if request.forms.get('id_filme') else avaliacao.id_filme
        avaliacao.id_usuario = int(request.forms.get('id_usuario')) if request.forms.get('id_usuario') else avaliacao.id_usuario

      
        self.avaliacao_model.update_avaliacao(avaliacao) 


    def delete_avaliacao(self, avaliacao_id): 
        self.avaliacao_model.delete_avaliacao(avaliacao_id)

    # metodo para perfil
    def get_all_avaliacoes_by_user_id(self, user_id):
       
        all_avaliacoes = self.avaliacao_model.get_all()
        user_specific_avaliacoes = []
        for avaliacao in all_avaliacoes:

            if hasattr(avaliacao, 'id_usuario') and avaliacao.id_usuario == user_id:
                user_specific_avaliacoes.append(avaliacao)
        return user_specific_avaliacoes