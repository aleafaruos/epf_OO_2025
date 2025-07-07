from bottle import Bottle, request, redirect, response
import json
from .base_controller import BaseController
from services.user_service import UserService
from services.avaliacao_service import AvaliacaoService
from services.api_service import TMDBService

class UserController(BaseController):

    def __init__(self, app):
        super().__init__(app)
        self.user_service = UserService()
        self.avaliacao_service = AvaliacaoService()
        self.tmdb_service = TMDBService()
        self.SESSION_COOKIE_NAME = 'user_session_id'
        self.setup_routes()

    def setup_routes(self):
        """Define todas as rotas relacionadas ao usuário."""
        self.app.route('/users/add', method='POST', callback=self.add_user)
        self.app.route('/login', method='POST', callback=self.do_login)
        self.app.route('/logout', method='GET', callback=self.do_logout)
        self.app.route('/profile', method='GET', callback=self.user_profile)
        self.app.route('/api/favorites/toggle', method='POST', callback=self.toggle_favorite_api)

    def add_user(self):
        """Cria um novo usuário a partir do formulário do modal."""
        try:
            new_user = self.user_service.save()
            if new_user:
                response.set_cookie(self.SESSION_COOKIE_NAME, str(new_user.id), path='/', httponly=True)
                return json.dumps({'success': True})
            else:
                raise ValueError("Não foi possível criar o usuário.")
        except ValueError as e:
            response.status = 400
            return json.dumps({'success': False, 'message': str(e)})

    def do_login(self):
        """Autentica o usuário a partir do formulário do modal."""
        email = request.forms.get('email')
        raw_password = request.forms.get('senha')
        user = self.user_service.check_credentials(email, raw_password)
        if user:
            response.set_cookie(self.SESSION_COOKIE_NAME, str(user.id), path='/', httponly=True)
            return json.dumps({'success': True})
        else:
            response.status = 401
            return json.dumps({'success': False, 'message': 'Email ou senha inválidos.'})

    def do_logout(self):
        """Faz o logout do usuário."""
        response.delete_cookie(self.SESSION_COOKIE_NAME, path='/')
        return self.redirect('/movies')

    def user_profile(self):
        user = self._get_logged_in_user()
        if not user:
            return self.redirect('/movies')
        
        favorite_movies_details = []
        if user.favorites:
            for movie_id in user.favorites:
                try:
                    movie_details = self.tmdb_service.get_movie_details(movie_id)
                    if movie_details:
                        favorite_movies_details.append(movie_details)
                except Exception as e:
                    print(f"Erro ao buscar filme favorito ID {movie_id}: {e}")
        
        user_reviews = self.avaliacao_service.get_all_avaliacoes_by_user_id(user.id)
        reviews_with_details = []
        for review in user_reviews:
            try:
                movie_details = self.tmdb_service.get_movie_details(review.id_filme)
                if movie_details:
                    review_data = review.to_dict()
                    review_data['movie_details'] = movie_details
                    reviews_with_details.append(review_data)
            except Exception as e:
                print(f"Erro ao buscar filme avaliado ID {review.id_filme}: {e}")

        reviews_with_details.sort(key=lambda r: r['id'], reverse=True)

        return self.render('user_profile', 
                           user=user, 
                           user_favorites=favorite_movies_details, 
                           user_reviews=reviews_with_details,
                           logged_in_user=user)

    def toggle_favorite_api(self):
        """Adiciona ou remove um filme dos favoritos de um usuário via API."""
        user = self._get_logged_in_user()
        if not user:
            response.status = 401
            return json.dumps({'success': False, 'message': 'Usuário não autenticado.'})
        
        movie_id = request.forms.get('movie_id')
        if not movie_id:
            response.status = 400
            return json.dumps({'success': False, 'message': 'ID do filme não fornecido.'})

        try:
            is_now_favorite = self.user_service.toggle_favorite(user.id, movie_id)
            return json.dumps({'success': True, 'isFavorite': is_now_favorite})
        except Exception as e:
            response.status = 500
            return json.dumps({'success': False, 'message': str(e)})

    def _get_logged_in_user(self):
        """Função auxiliar para pegar o usuário da sessão."""
        user_id_str = request.get_cookie(self.SESSION_COOKIE_NAME)
        if user_id_str:
            try:
                user_id = int(user_id_str)
                return self.user_service.get_by_id(user_id)
            except (ValueError, TypeError):
                return None
        return None

# Linhas de inicialização do controller que são necessárias para a importação
user_routes = Bottle()
user_controller = UserController(user_routes)