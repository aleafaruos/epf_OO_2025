from bottle import request 
from models.avaliacao import avaliacaoModel, Avaliacao 

class AvaliacaoService: 
    def __init__(self): 
        self.avaliacao_model = avaliacaoModel() 


    def get_all(self): 
        avaliacao = self.avaliacao_model.get_all() 
        return avaliacao 


    def save(self): 
        id = id.forms.get('id') 
        nota = request.forms.get('nota') 
        nome_usuario = request.forms.get('nome_usuario') 
        comentario = request.forms.get('comentario') 

        Avaliacao = Avaliacao(id=id, nota=nota, nome_usuario=nome_usuario, comentario=comentario) 
        self.avaliacao_model.add_avaliacao(Avaliacao) 


    def get_by_id(self, avaliacao_id): 
        return self.avaliacao_model.get_by_id(avaliacao_id) 


    def edit_avaliacao(self, avaliacao): 
        id = request.forms.get('id') 
        nota = request.forms.get('nota') 
        nome_usuario = request.forms.get('nome_usuario') 
        comentario = request.forms.get('comentario') 

        avaliacao.id = id 
        avaliacao.nota = nota 
        avaliacao.nome_usuario = nome_usuario 
        avaliacao.comentario = comentario 

        self.avaliacao_model.update_user(avaliacao) 


    def delete_avaliacao(self, avaliacao_id): 
        self.avaliacao_model.delete_user(avaliacao_id)