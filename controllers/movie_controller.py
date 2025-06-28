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
        # URL da API do TMDb para filmes populares em português
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={self.api_key}&language=pt-BR'
        
        movies = [] # Inicializa a lista de filmes
        error_message = None

        try:
            response = requests.get(url)
            response.raise_for_status() # Lança HTTPError para respostas 4xx/5xx
            data = response.json()
            
            # Adapta os dados da API para o seu modelo Movie (ou para o formato esperado pelo template)
            for item in data.get('results', []):
                movie_id = item.get('id')
                movie_name = item.get('title')
                movie_ano = item.get('release_date', '') # TMDb tem 'release_date'
                if movie_ano:
                    movie_ano = movie_ano[:4] # Pega apenas o ano
                poster_path = item.get('poster_path')
                full_poster = ""
                if poster_path:
                    full_poster = f"{self.image_base_url}{poster_path}"
                # Cria uma instância da sua classe Movie. Isso é útil para consistência com o resto do sistema.
                # Se Movie não tem um campo 'text' ou outros, ensure que o movies_form.tpl não os espera.
                    movies.append(Movie(id=movie_id, name=movie_name, ano=movie_ano,poster=full_poster))
                filme_resumo = item.get('overview', '')           # Extrai 'overview' da API para 'filme_resumo'
                filme_avaliacao_media = item.get('vote_average', 0.0) # Extrai 'vote_average' da API
                filme_numero_votos = item.get('vote_count', 0)     # Extrai 'vote_count' da API
                filme_popularidade = item.get('popularity', 0.0)   # Extrai 'popularity' da API

            # Passa todas as informações para o construtor do Movie, usando os NOMES EM PORTUGUÊS dos atributos
            movies.append(Movie(
                id=movie_id, 
                name=movie_name, 
                ano=movie_ano,
                poster=full_poster,
                resumo=filme_resumo,               # Passa a variável 'filme_resumo' para o atributo 'resumo'
                avaliacao_media=filme_avaliacao_media,   # E assim por diante...
                numero_votos=filme_numero_votos,
                popularidade=filme_popularidade
            ))
        except requests.exceptions.RequestException as e:
            # Captura erros de rede ou de status HTTP (ex: 404, 500)
            print(f"Erro ao conectar ou receber dados da API do TMDb: {e}")
            error_message = "Não foi possível carregar os filmes populares da API do TMDb."
            # Opcional: Se a API falhar, você pode tentar carregar do seu JSON local como fallback
            # movies = self.movie_service.get_all()
        except KeyError as e:
            # Captura erros se a estrutura JSON da API for inesperada
            print(f"Erro ao processar dados da API (chave ausente): {e}")
            error_message = "Formato de dados da API inesperado. Tente novamente mais tarde."
        except Exception as e:
            # Captura outros erros inesperados
            print(f"Ocorreu um erro inesperado: {e}")
            error_message = "Ocorreu um erro inesperado ao carregar os filmes."

        return self.render('movies', movies=movies, error_message=error_message)



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
            # POST - salvar edição
            self.movie_service.edit_movie(movie)
            self.redirect('/movies')


    def delete_movie(self, movie_id):
        self.movie_service.delete_movie(movie_id)
        self.redirect('/movies')


movie_routes = Bottle()
movie_controller = movieController(movie_routes)

