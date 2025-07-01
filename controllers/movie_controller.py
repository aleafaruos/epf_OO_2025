from bottle import Bottle, request,redirect,response
from .base_controller import BaseController
from services.movie_service import movieService, Movie
import requests
from services.user_service import UserService # <--- IMPORT DO UserService ADICIONADO/MANTIDO AQUI

class movieController(BaseController):
    def __init__(self, app):
        # --- ALTERAÇÃO AQUI: Garante que o nome do cookie é o mesmo do UserController ---
        self.user_service = UserService() 
        self.SESSION_COOKIE_NAME = 'user_session_id' # AGORA CONSISTENTE COM USERCONTROLLER
        # -----------------------------------------------------------------

        super().__init__(app) # Chama o construtor da classe base

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
        self.app.route('/filmes/<movie_id:int>/avaliar', method=['GET', 'POST'], callback=self.evaluate_movie)


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

    # --- MÉTODO AUXILIAR PARA OBTER O USUÁRIO LOGADO (COM DEBUG) ---
    def _get_logged_in_user(self):
        print(f"\n--- DEBUG VERIFICAÇÃO LOGIN FILMES INICIADO ---")
        user_id_str = request.get_cookie(self.SESSION_COOKIE_NAME)
        print(f"Cookie '{self.SESSION_COOKIE_NAME}' lido: '{user_id_str}'")

        if user_id_str:
            try:
                user_id = int(user_id_str)
                user = self.user_service.get_by_id(user_id)
                if user:
                    print(f"Usuário encontrado pelo ID do cookie: {user.name}")
                else:
                    print("ID do cookie inválido: Usuário não encontrado no serviço.")
                    response.delete_cookie(self.SESSION_COOKIE_NAME, path='/') # Limpa cookie inválido
                print(f"--- DEBUG VERIFICAÇÃO LOGIN FILMES ENCERRADO ---\n")
                return user
            except (ValueError, TypeError):
                print("Erro: Cookie ID não é um número. Limpando cookie.")
                response.delete_cookie(self.SESSION_COOKIE_NAME, path='/')
                print(f"--- DEBUG VERIFICAÇÃO LOGIN FILMES ENCERRADO ---\n")
                return None
        print("Nenhum cookie de sessão encontrado.")
        print(f"--- DEBUG VERIFICAÇÃO LOGIN FILMES ENCERRADO ---\n")
        return None
    # --- FIM DO MÉTODO AUXILIAR ---

    def evaluate_movie(self, movie_id):
        movie = self.movie_service.get_by_id(movie_id)

        # 1. Verificação de Usuário Logado
        logged_in_user = self._get_logged_in_user() 
        if not logged_in_user:
            return self.redirect(f'/login?next=/filmes/{movie_id}/avaliar') 
            
        # 2. Busca do Filme (Local e API Externa)
        if not movie:
            try:
                url_api_detail = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={self.api_key}&language=pt-BR'
                response_api = requests.get(url_api_detail)
                response_api.raise_for_status() 
                data = response_api.json()

                movie = Movie(
                    id=data.get('id'),
                    name=data.get('title'),
                    ano=data.get('release_date', '')[:4] if data.get('release_date') else '',
                    poster=f"{self.image_base_url}{data.get('poster_path')}" if data.get('poster_path') else "",
                    resumo=data.get('overview', ''),
                    avaliacao_media=data.get('vote_average', 0.0),
                    numero_votos=data.get('vote_count', 0),
                    popularidade=data.get('popularity', 0.0)
                )
            except requests.exceptions.RequestException as e:
                print(f"Erro ao buscar filme {movie_id} na API do TMDb: {e}")
                return "Não foi possível encontrar os detalhes do filme na API do TMDb."
            except Exception as e:
                print(f"Erro inesperado ao processar dados do filme {movie_id} da API: {e}")
                return "Ocorreu um erro inesperado ao carregar os detalhes do filme."

        # 3. Tratamento de Filme Não Encontrado
        if not movie: 
            return "Filme não encontrado para avaliação."

        # 4. Requisição GET: Exibir Formulário
        if request.method == 'GET':
            return self.render('evaluate_movie_form', movie=movie)
        
        # 5. Requisição POST: Processar Avaliação
        else: # POST
            try:
                valor_digitado = request.forms.get('avaliacao').replace(',', '.')
                nova_avaliacao = float(valor_digitado)

                movie.avaliacao_media = nova_avaliacao 
                
                self.movie_service.edit_movie(movie) 

                self.redirect(f'/movies?message=Filme {movie.name} avaliado com sucesso!')
            except ValueError:
                return self.render('evaluate_movie_form', movie=movie, error_message="Avaliação inválida. Por favor, insira um número.")
            except Exception as e:
                return self.render('evaluate_movie_form', movie=movie, error_message=f"Erro ao salvar avaliação: {e}")


movie_routes = Bottle()
movie_controller = movieController(movie_routes)