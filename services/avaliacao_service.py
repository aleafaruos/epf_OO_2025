from bottle import request
from models.avaliacao import avaliacaoModel, Avaliacao
from services.user_service import UserService

class AvaliacaoService:
    def __init__(self):
        self.avaliacao_model = avaliacaoModel()

    def get_all(self):
        return self.avaliacao_model.get_all()

    def save(self):
        avaliacoes = self.avaliacao_model.get_all()
        last_id = max([a.id for a in avaliacoes], default=0) if avaliacoes else 0
        new_id = last_id + 1

        id_usuario = request.forms.get('id_usuario')
        id_filme = request.forms.get('id_filme')
        nota = request.forms.get('nota')
        comentario = request.forms.get('comentario', '')

        if not id_usuario or not id_filme or not nota:
            return None

        nova_avaliacao = Avaliacao(
            id=new_id,
            nota=nota,
            comentario=comentario,
            id_filme=int(id_filme),
            id_usuario=int(id_usuario)
        )

        self.avaliacao_model.add_avaliacao(nova_avaliacao)
        return nova_avaliacao

    def get_by_id(self, avaliacao_id):
        return self.avaliacao_model.get_by_id(avaliacao_id)

    def edit_avaliacao(self, avaliacao: Avaliacao):
        avaliacao.nota = request.forms.get('nota', avaliacao.nota)
        avaliacao.comentario = request.forms.get('comentario', avaliacao.comentario)
        self.avaliacao_model.update_avaliacao(avaliacao)

    def delete_avaliacao(self, avaliacao_id):
        self.avaliacao_model.delete_avaliacao(avaliacao_id)

    def get_all_avaliacoes_by_user_id(self, user_id):
        return [ava for ava in self.get_all() if ava.id_usuario == user_id]
    
    def get_reviews_with_user_info(self, movie_id):
        user_service = UserService()
        movie_reviews = [ava for ava in self.get_all() if ava.id_filme == movie_id]
        
        reviews_with_user_info = []
        for review in movie_reviews:
            user = user_service.get_by_id(review.id_usuario)
            review_data = review.to_dict()
            review_data['nome_usuario'] = user.name if user else 'Usuário Anônimo'
            reviews_with_user_info.append(review_data)
            
        return reviews_with_user_info