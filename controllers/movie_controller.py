
from bottle import Bottle, request, redirect
import requests
from .base_controller import BaseController
from services.movie_service import movieService
from services.user_service import UserService
from services.api_service import TMDBService
from services.avaliacao_service import AvaliacaoService
from models.movie import Movie

class movieController(BaseController):

    def __init__(self, app):
        super().__init__(app)
        self.user_service = UserService()
        self.movie_service = movieService()
        self.avaliacao_service = AvaliacaoService()
        self.tmdb_service = TMDBService() 
        self.SESSION_COOKIE_NAME = 'user_session_id'
        self.setup_routes()

    def setup_routes(self):
        """ Registra todas as rotas para o controller de filmes. """
        self.app.route('/movies', method='GET', callback=self.list_movies)
        self.app.route('/movies/<movie_id:int>', method='GET', callback=self.movie_details)
        self.app.route('/filme/favoritar', method='POST', callback=self.handle_favorite)

    def list_movies(self):
        termo_busca = request.query.get('termo_busca', '').strip()
        movies = []
        error_message = None
        try:
            movies_data = self.tmdb_service.search_movies(termo_busca) if termo_busca else self.tmdb_service.get_popular_movies()
            for item in movies_data:
                poster_path = item.get('poster_path')
                item['poster'] = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ''
                movies.append(Movie.from_dict(item))
        except requests.exceptions.RequestException as e:
            error_message = f"Erro ao conectar à API do TMDb: {e}"
        logged_in_user = self._get_logged_in_user()
        return self.render('movies', movies=movies, error_message=error_message, logged_in_user=logged_in_user, termo_busca=termo_busca)

    def movie_details(self, movie_id):
        movie_data = {}
        reviews = []
        error_message = None
        try:
            movie_data = self.tmdb_service.get_movie_details(movie_id)
            if movie_data:
                poster_path = movie_data.get('poster_path')
                movie_data['poster_backdrop_url'] = f"https://image.tmdb.org/t/p/original{poster_path}" if poster_path else ''
                movie_data['poster_main_url'] = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ''
            reviews = self.avaliacao_service.get_reviews_with_user_info(movie_id)
        except requests.exceptions.RequestException as e:
            error_message = f"Erro ao buscar detalhes do filme: {e}"
        logged_in_user = self._get_logged_in_user()
        return self.render('movie_details', movie=movie_data, reviews=reviews, error_message=error_message, logged_in_user=logged_in_user)
        
    def handle_favorite(self):
        movie_id_str = request.forms.get('id_filme')
        user = self._get_logged_in_user()

        if user and movie_id_str:
            self.user_service.toggle_favorite(user.id, int(movie_id_str))
        
        # Redireciona o usuário de volta para a página do filme.
        return redirect(f'/movies/{movie_id_str}')

    def _get_logged_in_user(self):
        user_id_str = request.get_cookie(self.SESSION_COOKIE_NAME)
        if user_id_str:
            try:
                user_id = int(user_id_str)
                return self.user_service.get_by_id(user_id)
            except (ValueError, TypeError): 
                return None
        return None

# Esta parte é necessária para que o __init__.py possa importar 'movie_routes'
movie_routes = Bottle()
movie_controller = movieController(movie_routes)