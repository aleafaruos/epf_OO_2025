# controllers/movie_controller.py

from bottle import Bottle, request, redirect, response, abort, HTTPResponse # Importação única e correta
from .base_controller import BaseController
from services.movie_service import movieService
from models.movie import Movie
import requests
from services.user_service import UserService
from services.api_service import TMDBService

class movieController(BaseController):
    def __init__(self, app):
        self.user_service = UserService() 
        self.SESSION_COOKIE_NAME = 'user_session_id' 

        super().__init__(app)

        self.setup_routes()
        self.movie_service = movieService()
        self.tmdb_service = TMDBService()
        self.api_key = '837d294758fed763def26fe173fc765f' 
        self.image_base_url = 'https://image.tmdb.org/t/p/w500' 


    def setup_routes(self):
        self.app.route('/movies', method='GET', callback=self.list_movies)
        self.app.route('/movies/add', method=['GET', 'POST'], callback=self.add_movie)
        self.app.route('/movies/edit/<movie_id:int>', method=['GET', 'POST'], callback=self.edit_movie)
        self.app.route('/movies/delete/<movie_id:int>', method='POST', callback=self.delete_movie)
        self.app.route('/filmes/<movie_id:int>/avaliar', method=['GET', 'POST'], callback=self.evaluate_movie)
        self.app.route('/filmes', method='GET', callback=lambda: redirect('/movies'))


    def list_movies(self):
        self.check_auth()
        termo_busca = request.query.get('termo_busca', '').strip() 
        
        all_movies_by_id = {} 
        error_message = None

        local_movies = self.movie_service.get_all() 
        for movie in local_movies:
            all_movies_by_id[movie.id] = movie 

        try:
            movies_from_api_raw = []
            if termo_busca:
                movies_from_api_raw = self.tmdb_service.search_movies(termo_busca)
            else:
                movies_from_api_raw = self.tmdb_service.get_popular_movies()

            for item_data in movies_from_api_raw:
                movie_id = item_data.get('id')
                
                if movie_id:
                    processed_movie = self.movie_service.save_or_get_movie(item_data)
                    all_movies_by_id[processed_movie.id] = processed_movie 
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar ou receber dados da API do TMDb: {e}")
            error_message = "Não foi possível carregar filmes da API do TMDb."
        except KeyError as e:
            print(f"Erro ao processar dados da API (chave ausente): {e}")
            error_message = "Formato de dados da API inesperado. Tente novamente mais tarde."
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao carregar filmes: {e}")
            error_message = "Ocorreu um erro inesperado ao carregar os filmes."

        movies_to_display = []
        if termo_busca:
            termo_lower = termo_busca.lower()
            for movie in all_movies_by_id.values():
                if termo_lower in movie.name.lower() or \
                   (movie.resumo and termo_lower in movie.resumo.lower()):
                    movies_to_display.append(movie)
        else:
            movies_to_display = list(all_movies_by_id.values())

        movies_to_display.sort(key=lambda m: m.name.lower())

        return self.render('movies', movies=movies_to_display, error_message=error_message, termo_busca=termo_busca)

    def add_movie(self):
        self.check_auth()
        if request.method == 'GET':
            return self.render('movies_form', movie=None, action="/movies/add")
        else:
            self.movie_service.save() 
            self.redirect('/movies')


    def edit_movie(self, movie_id):
        self.check_auth()
        movie = self.movie_service.get_by_id(movie_id)
        if not movie:
            return "Filme não encontrado"

        if request.method == 'GET':
            return self.render('movies_form', movie=movie, action=f"/movies/edit/{movie_id}")
        else:
            self.movie_service.edit_movie(movie_id)
            self.redirect('/movies')


    def delete_movie(self, movie_id):
        self.check_auth()
        self.movie_service.delete_movie(movie_id)
        self.redirect('/movies')

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
                    response.delete_cookie(self.SESSION_COOKIE_NAME, path='/') 
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

    def check_auth(self):
        user = self._get_logged_in_user()
        if not user:
            redirect('/login')

    def evaluate_movie(self, movie_id):
        print("\n--- DEBUG: evaluate_movie INICIADO (Versão 2025-07-03 - REVISÃO FINAL DE REPLACE) ---")
        logged_in_user = self._get_logged_in_user() 
        if not logged_in_user:
            return self.redirect(f'/login?next=/filmes/{movie_id}/avaliar') 
            
        movie = self.movie_service.get_by_id(movie_id)

        if not movie:
            try:
                movie_data_from_api = self.tmdb_service.get_movie_details(movie_id)
                
                if movie_data_from_api:
                    movie = self.movie_service.save_or_get_movie(movie_data_from_api)
                else:
                    print(f"DEBUG: Filme {movie_id} não encontrado na API do TMDb.")
                    return "Filme não encontrado para avaliação."
            except requests.exceptions.RequestException as e:
                print(f"Erro ao buscar filme {movie_id} na API do TMDb: {e}")
                return "Não foi possível encontrar os detalhes do filme na API do TMDb."
            except Exception as e:
                print(f"Erro inesperado ao processar dados do filme {movie_id} da API: {e}")
                return "Ocorreu um erro inesperado ao carregar os detalhes do filme."

        if not movie: 
            return "Filme não encontrado para avaliação."
            
        if request.method == 'GET':
            return self.render('evaluate_movie_form', movie=movie)
        
        else: # POST
            try:
                valor_do_form = request.forms.get('avaliacao') 
                print(f"DEBUG: Valor recebido do formulário: '{valor_do_form}' (type: {type(valor_do_form)})")
                
                if valor_do_form is None or str(valor_do_form).strip() == '':
                    raise ValueError("Avaliação não pode ser vazia.")
                
                string_para_processar = str(valor_do_form) 
                print(f"DEBUG: String para processar (após str()): '{string_para_processar}' (type: {type(string_para_processar)})")

                valor_final_string = string_para_processar.replace(',', '.') 
                print(f"DEBUG: Valor após replace: '{valor_final_string}' (type: {type(valor_final_string)})")

                nova_avaliacao = float(valor_final_string)
                print(f"DEBUG: Nova Avaliação (float): {nova_avaliacao} (type: {type(nova_avaliacao)})")

                if not (0 <= nova_avaliacao <= 10):
                    raise ValueError("Avaliação deve ser entre 0 e 10.")

                comentario = request.forms.get('comentario', '') 
                self.movie_service.update_movie_rating(movie.id, nova_avaliacao, comentario) 

                # Alteração 1: Usando abort(redirect(...))
                abort(redirect(f'/movies?message=Filme {movie.name} avaliado com sucesso!'))
            except ValueError as ve:
                print(f"ERRO DE VALIDAÇÃO AO AVALIAR FILME: {ve}")
                return self.render('evaluate_movie_form', movie=movie, error_message=f"Erro de validação: {ve}")
            except Exception as e:
                # Alteração 2: Trata HTTPResponse especificamente, re-lançando-o
                if isinstance(e, HTTPResponse):
                    print(f"DEBUG: HTTPResponse capturada, re-lançando para o Bottle: {e}")
                    raise e
                else:
                    print(f"ERRO INESPERADO AO AVALIAR FILME: [Tipo: {type(e).__name__}, Mensagem: '{e}']") 
                    return self.render('evaluate_movie_form', movie=movie, error_message=f"Ocorreu um erro ao salvar sua avaliação: {e}")

movie_routes = Bottle()
movie_controller = movieController(movie_routes)