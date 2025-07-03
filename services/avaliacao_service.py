# services/avaliacao_service.py
from bottle import request # Mantenha o request se ainda for usado em outros métodos

# Verifique estas importações:
from models.avaliacao import Avaliacao, avaliacaoModel # Certifique-se que Avaliacao (com 'A' maiúsculo) e avaliacaoModel estão sendo importados
from models.movie import Movie # Certifique-se que a classe Movie (com 'M' maiúsculo) está sendo importada

class AvaliacaoService:
    def __init__(self):
        self.avaliacao_model = avaliacaoModel() # Instancia o novo avaliacaoModel

    # 1. Método para obter todas as avaliações de um usuário específico para o perfil
    def get_all_avaliacoes_by_user_id(self, user_id):
        # Agora você chama o novo método do seu avaliacaoModel que já retorna
        # as avaliações com os detalhes básicos dos filmes
        all_avaliacoes_with_movie_data = self.avaliacao_model.get_all_avaliacoes_from_movies()

        user_specific_reviews_for_profile = []
        for item_data in all_avaliacoes_with_movie_data:
            avaliacao_obj = item_data['avaliacao'] # O objeto Avaliacao real
            
            # Compara o user_id do objeto Avaliacao com o user_id passado
            if avaliacao_obj.user_id == user_id:
                # Cria um objeto Movie simplificado com base nos dados que o model já trouxe
                simplified_movie_obj = Movie(
                    id=item_data['movie_id'],
                    name=item_data['movie_name'],
                    ano=item_data['movie_ano'],
                    poster=item_data['movie_poster']
                    # Você não precisa de outros campos como resumo, avaliacao_media etc. para o perfil aqui
                )
                user_specific_reviews_for_profile.append({
                    'review': avaliacao_obj, # O objeto Avaliacao
                    'movie': simplified_movie_obj # O objeto Movie simplificado
                })
        return user_specific_reviews_for_profile

    # 2. Método para salvar uma nova avaliação
    def save(self):
        # Recupera os dados do formulário de avaliação
        movie_id_str = request.forms.get('id_filme')
        current_user_id_str = request.forms.get('id_usuario') # ID do usuário logado vindo do formulário
        user_name_from_form = request.forms.get('nome_usuario')
        nota_from_form = request.forms.get('nota')
        comentario_from_form = request.forms.get('comentario') # Este é o campo de texto do comentário

        if not movie_id_str or not current_user_id_str:
            print("Erro: ID do filme ou do usuário ausente no formulário de avaliação.")
            return False

        try:
            movie_id = int(movie_id_str)
            user_id = int(current_user_id_str)
            # Converte a nota para float, pois é uma avaliação
            nota = float(nota_from_form) 
        except ValueError:
            print("Erro: ID de filme, ID de usuário ou nota inválidos (não são números).")
            return False

        # Cria uma nova instância de Avaliacao com os dados corretos
        nova_avaliacao_obj = Avaliacao(
            user_id=user_id,
            user_name=user_name_from_form,
            avaliacao=nota, # Atribuindo a nota ao campo 'avaliacao'
            comentario_texto=comentario_from_form # Atribuindo o comentário ao campo 'comentario_texto'
        )
        
        # Chama o método do avaliacaoModel para adicionar a avaliação ao filme
        return self.avaliacao_model.add_avaliacao_to_movie(movie_id, nova_avaliacao_obj)

    # REMOVA os métodos antigos que lidavam com avaliacao.json:
    # def get_all(self):
    # def get_by_id(self, avaliacao_id):
    # def edit_avaliacao(self, avaliacao):
    # def delete_avaliacao(self, avaliacao_id):
    # Se você precisar de funcionalidades de editar/deletar avaliações no futuro,
    # elas deverão ser implementadas de forma que interajam com o movies.json
    # (provavelmente chamando métodos específicos no avaliacaoModel para isso).