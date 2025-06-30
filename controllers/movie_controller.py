from bottle import Bottle, request,redirect,response
from .base_controller import BaseController
from services.movie_service import movieService, Movie
import requests

class movieController(BaseController):
    def __init__(self, app):
        super().__init__(app)

        self.setup_routes()
        self.movie_service = movieService()
        self.api_key = '837d294758fed763def26fe173fc765f' 
        self.image_base_url = 'https://image.tmdb.org/t/p/w500' 


    # Rotas movie
    def setup_routes(self):
        self.app.route('/movies', method='GET', callback=self.list_movies)
        self.app.route('/movies/add', method=['GET', 'POST'], callback=self.add_movie)
        self.app.route('/movies/edit/<movie_id:int>', method=['GET', 'POST'], callback=self.edit_movie)
        self.app.route('/movies/delete/<movie_id:int>', method='POST', callback=self.delete_movie)


    def list_movies(self):

        termo_busca = request.query.get('termo_busca', '').strip() 
        
        all_movies_by_id = {} 
        error_message = None

        try:
            if termo_busca:
                url_api = f'https://api.themoviedb.org/3/search/movie?api_key={self.api_key}&language=pt-BR&query={termo_busca}'
            else:
                url_api = f'https://api.themoviedb.org/3/movie/popular?api_key={self.api_key}&language=pt-BR'
            
            response = requests.get(url_api)
            response.raise_for_status() 
            data = response.json()
            
            for item in data.get('results', []):
                movie_id = item.get('id')
                movie_name = item.get('title')
                movie_ano = item.get('release_date', '') 
                if movie_ano:
                    movie_ano = movie_ano[:4] 
                poster_path = item.get('poster_path')
                full_poster = f"{self.image_base_url}{poster_path}" if poster_path else ""
                
                filme_resumo = item.get('overview', '') 
                filme_avaliacao_media = item.get('vote_average', 0.0)
                filme_numero_votos = item.get('vote_count', 0)
                filme_popularidade = item.get('popularity', 0.0)

                movie_obj = Movie(
                    id=movie_id, 
                    name=movie_name, 
                    ano=movie_ano,
                    poster=full_poster,
                    resumo=filme_resumo, 
                    avaliacao_media=filme_avaliacao_media, 
                    numero_votos=filme_numero_votos,
                    popularidade=filme_popularidade
                )
                all_movies_by_id[movie_id] = movie_obj 
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar ou receber dados da API do TMDb: {e}")
            error_message = "Não foi possível carregar os filmes populares da API do TMDb."
        except KeyError as e:
            print(f"Erro ao processar dados da API (chave ausente): {e}")
            error_message = "Formato de dados da API inesperado. Tente novamente mais tarde."
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            error_message = "Ocorreu um erro inesperado ao carregar os filmes."

        # Carrega os filmes
        local_movies = self.movie_service.get_all(termo_busca) 
        for movie in local_movies:
            all_movies_by_id[movie.id] = movie 

        movies_to_display = list(all_movies_by_id.values())
        movies_to_display.sort(key=lambda m: m.name.lower())

        return self.render('movies', movies=movies_to_display, error_message=error_message, termo_busca=termo_busca)


    def add_movie(self):
        if request.method == 'GET':
            return self.render('movies_form', movie=None, action="/movies/add")
        else:
            # POST - salvar usuário
            self.movie_service.save()
            self.redirect('/movies')


    def edit_movie(self, movie_id):
        movie = self.movie_service.get_by_id(movie_id)
        if not movie:
            return "Filme não encontrado"

        if request.method == 'GET':
            return self.render('movies_form', movie=movie, action=f"/movies/edit/{movie_id}")
        else:
            
            self.movie_service.edit_movie(movie)
            self.redirect('/movies')


    def delete_movie(self, movie_id):
        self.movie_service.delete_movie(movie_id)
        self.redirect('/movies')


movie_routes = Bottle()
movie_controller = movieController(movie_routes)

