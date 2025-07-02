from bottle import Bottle, request, redirect, response, HTTPError # Importa HTTPError para lidar com 404
import requests # NOVO: Importa a biblioteca requests para fazer chamadas HTTP externas

from .base_controller import BaseController
from services.user_service import UserService
from services.avaliacao_service import AvaliacaoService # Importa AvaliacaoService (corrigido o nome do arquivo se necessário)
from services.movie_service import movieService # Importa movieService para pegar detalhes dos filmes
from models.movie import Movie # NOVO: Importa a CLASSE Movie para criar objetos Movie

class UserController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.user_service = UserService()
        self.avaliacao_service = AvaliacaoService() # Instancia AvaliacaoService
        self.movie_service = movieService() # Instancia movieService
        self.SESSION_COOKIE_NAME = 'user_session_id'
        self.setup_routes()

    # Rotas User
    def setup_routes(self):
        self.app.route('/users', method='GET', callback=self.list_users)
        self.app.route('/users/add', method=['GET', 'POST'], callback=self.add_user)
        self.app.route('/users/edit/<user_id:int>', method=['GET', 'POST'], callback=self.edit_user)
        self.app.route('/users/delete/<user_id:int>', method='POST', callback=self.delete_user)
        self.app.route('/login', method='GET', callback=self.login_form)
        self.app.route('/login', method='POST', callback=self.do_login)
        self.app.route('/logout', method='GET', callback=self.do_logout)
        self.app.route('/profile', method='GET', callback=self.user_profile)
        self.app.route('/users/<user_id:int>/profile', method='GET', callback=self.user_profile_by_id)
        
    def list_users(self):
        logged_in_user = self.get_logged_in_user()
        if not logged_in_user:
            return self.redirect('/login')
        
        users = self.user_service.get_all()
        return self.render('users', users=users, logged_in_user=logged_in_user)

    def add_user(self):
        if request.method == 'GET':
            return self.render('user_form', user=None, action="/users/add")
        else:
            self.user_service.save() 
            self.redirect('/users')

    def edit_user(self, user_id):
        logged_in_user = self.get_logged_in_user()
        if not logged_in_user:
            return self.redirect('/login')
        
        user = self.user_service.get_by_id(user_id)
        if not user:
            return "Usuário não encontrado"

        if request.method == 'GET':
            return self.render('user_form', user=user, action=f"/users/edit/{user_id}")
        else:
            self.user_service.edit_user(user)
            self.redirect('/users')

    def delete_user(self, user_id):
        logged_in_user = self.get_logged_in_user()
        if not logged_in_user:
            return self.redirect('/login')
        
        self.user_service.delete_user(user_id)
        self.redirect('/users')

    def do_logout(self):
        response.delete_cookie(self.SESSION_COOKIE_NAME, path='/')
        self.redirect('/login')

    def get_logged_in_user(self):
        user_id_str = request.get_cookie(self.SESSION_COOKIE_NAME)
        if user_id_str:
            try:
                user_id = int(user_id_str)
                user = self.user_service.get_by_id(user_id)
                if user:
                    return user
                else:
                    response.delete_cookie(self.SESSION_COOKIE_NAME, path='/')
                    return None
            except (ValueError, TypeError):
                response.delete_cookie(self.SESSION_COOKIE_NAME, path='/')
                return None
        return None

    def login_form(self):
        next_url = request.query.get('next', '')
        return self.render('login_form', email='', error_message='', next_url=next_url) 

    def do_login(self):
        email = request.forms.get('email')
        raw_password = request.forms.get('senha')

        print(f"\n--- DEBUG LOGIN INICIADO ---")
        print(f"Tentativa de login para email: {email}")

        user = self.user_service.check_credentials(email, raw_password)

        if user:
            print(f"Usuário {user.name} logado com sucesso!")
            response.set_cookie(self.SESSION_COOKIE_NAME, str(user.id), path='/', httponly=True)
            
            next_url = request.forms.get('next')

            print(f"Valor do parâmetro 'next' na URL (POST): '{next_url}'")

            if next_url:
                print(f"Redirecionando para: {next_url}")
                return self.redirect(next_url)
            else:
                print("Nenhum 'next' encontrado. Redirecionando para /users")
                return self.redirect('/users')

        else:
            error = "Email ou senha inválidos."
            print(f"Falha no login para {email}. Erro: {error}")
            print(f"--- DEBUG LOGIN ENCERRADO ---\n")
            return self.render('login_form', email=email, error_message=error)

    # metodo da Página de Perfil do Usuário Logado ---
    def user_profile(self):
        logged_in_user = self.get_logged_in_user()
        if not logged_in_user:
            return self.redirect('/login?next=/profile') # Redireciona para login se não estiver logado

        # Pega todas as avaliações feitas por este usuário
        user_reviews = self.avaliacao_service.get_all_avaliacoes_by_user_id(logged_in_user.id)
        
        # Cria uma lista para armazenar as avaliações com os detalhes do filme
        reviews_with_movie_details = []
        for review in user_reviews:
            movie_from_local_data = self.movie_service.get_by_id(review.id_filme)
            
            # Se o filme não for encontrado localmente, tenta buscar na API TMDB
            if not movie_from_local_data:
                try:
                    # Chave da API e URL base devem vir de um arquivo de configuração ou ser passadas.
                    # Por simplicidade, usando valores fixos por enquanto.
                    api_key = '837d294758fed763def26fe173fc765f' 
                    image_base_url = 'https://image.tmdb.org/t/p/w500' 
                    url_api_detail = f'https://api.themoviedb.org/3/movie/{review.id_filme}?api_key={api_key}&language=pt-BR'
                    
                    # CORREÇÃO CRÍTICA: Usar requests.get() da biblioteca 'requests'
                    response_api = requests.get(url_api_detail)
                    response_api.raise_for_status() # Levanta um HTTPError para 4xx/5xx responses
                    data = response_api.json()

                    # CORREÇÃO: Chamar a CLASSE Movie (com 'M' maiúsculo)
                    movie_details_from_api = Movie( 
                        id=data.get('id'),
                        name=data.get('title'),
                        ano=data.get('release_date', '')[:4] if data.get('release_date') else '',
                        poster=f"{image_base_url}{data.get('poster_path')}" if data.get('poster_path') else "",
                        resumo=data.get('overview', ''),
                        avaliacao_media=data.get('vote_average', 0.0),
                        numero_votos=data.get('vote_count', 0),
                        popularidade=data.get('popularity', 0.0)
                    )
                    reviews_with_movie_details.append({
                        'review': review,
                        'movie': movie_details_from_api
                    })
                except requests.exceptions.RequestException as e:
                    print(f"Erro de requisição ao buscar detalhes do filme {review.id_filme} da API para perfil: {e}")
                    # Adiciona uma entrada com filme genérico para não quebrar a exibição
                    reviews_with_movie_details.append({
                        'review': review,
                        'movie': Movie(id=review.id_filme, name="Filme Não Encontrado", ano="", poster="", resumo="Detalhes não disponíveis.") 
                    })
                except Exception as e:
                    print(f"Erro inesperado ao processar filme {review.id_filme} da API para perfil: {e}")
                    reviews_with_movie_details.append({
                        'review': review,
                        'movie': Movie(id=review.id_filme, name="Filme Não Encontrado", ano="", poster="", resumo="Detalhes não disponíveis.") 
                    })
            else: # Se o filme for encontrado localmente
                reviews_with_movie_details.append({
                    'review': review,
                    'movie': movie_from_local_data
                })
        
        # Renderiza o template de perfil do usuário
        return self.render('user_profile', 
                            user=logged_in_user, 
                            reviews=reviews_with_movie_details)

    #metodo Página de Perfil de OUTRO Usuário (Opcional) ---
    def user_profile_by_id(self, user_id):
        logged_in_user = self.get_logged_in_user()
        if not logged_in_user:
            return self.redirect(f'/login?next=/users/{user_id}/profile')

        target_user = self.user_service.get_by_id(user_id)
        if not target_user:
            return HTTPError(404, "Usuário não encontrado.") 

        user_reviews = self.avaliacao_service.get_all_avaliacoes_by_user_id(target_user.id)
        
        reviews_with_movie_details = []
        for review in user_reviews:
            movie_from_local_data = self.movie_service.get_by_id(review.id_filme)
            if not movie_from_local_data: 
                try:
                    api_key = '837d294758fed763def26fe173fc765f' 
                    image_base_url = 'https://image.tmdb.org/t/p/w500' 
                    url_api_detail = f'https://api.themoviedb.org/3/movie/{review.id_filme}?api_key={api_key}&language=pt-BR'
                    
                    response_api = requests.get(url_api_detail) 
                    response_api.raise_for_status() 
                    data = response_api.json()
                    
                    movie_details_from_api = Movie(
                        id=data.get('id'), name=data.get('title'), ano=data.get('release_date', '')[:4],
                        poster=f"{image_base_url}{data.get('poster_path')}" if data.get('poster_path') else "",
                        resumo=data.get('overview', ''), avaliacao_media=data.get('vote_average', 0.0),
                        numero_votos=data.get('vote_count', 0), popularidade=data.get('popularity', 0.0)
                    )
                    reviews_with_movie_details.append({
                        'review': review,
                        'movie': movie_details_from_api
                    })
                except requests.exceptions.RequestException as e:
                    print(f"Erro de requisição ao buscar detalhes do filme {review.id_filme} da API para perfil de outro usuário: {e}")
                    reviews_with_movie_details.append({
                        'review': review,
                        'movie': Movie(id=review.id_filme, name="Filme Não Encontrado", ano="", poster="", resumo="Detalhes não disponíveis.") 
                    })
                except Exception as e:
                    print(f"Erro inesperado ao processar filme {review.id_filme} da API para perfil de outro usuário: {e}")
                    reviews_with_movie_details.append({
                        'review': review,
                        'movie': Movie(id=review.id_filme, name="Filme Não Encontrado", ano="", poster="", resumo="Detalhes não disponíveis.") 
                    })
            else: 
                reviews_with_movie_details.append({
                    'review': review,
                    'movie': movie_from_local_data
                })

        return self.render('user_profile', 
                            user=target_user, 
                            reviews=reviews_with_movie_details)


user_routes = Bottle()
user_controller = UserController(user_routes)