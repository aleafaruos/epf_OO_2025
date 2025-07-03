# controllers/user_controller.py
from bottle import Bottle, request, redirect, response, HTTPError # Importa HTTPError para lidar com 404
import requests # Importa a biblioteca requests para fazer chamadas HTTP externas

from .base_controller import BaseController
from services.user_service import UserService
from services.avaliacao_service import AvaliacaoService # Importa AvaliacaoService
from services.movie_service import movieService # Importa movieService
from models.movie import Movie # Importa a CLASSE Movie para criar objetos Movie

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

        # Pega todas as avaliações feitas por este usuário.
        # O 'avaliacao_service' agora já retorna uma lista de dicionários,
        # onde cada item é {'review': Avaliacao_obj, 'movie': Movie_obj}.
        # Isso já é o formato que o template 'user_profile' espera.
        reviews_for_template = self.avaliacao_service.get_all_avaliacoes_by_user_id(logged_in_user.id)
        
        # --- LINHAS DE DEBUG: ADICIONE ESTAS 4 LINHAS ---
        print("\n--- DEBUG: reviews_for_template no user_controller.py ---")
        print(f"Tipo de reviews_for_template: {type(reviews_for_template)}")
        if reviews_for_template:
            print(f"Tipo do primeiro item: {type(reviews_for_template[0])}")
            if isinstance(reviews_for_template[0], dict):
                print(f"Chaves do primeiro item: {reviews_for_template[0].keys()}")
                if 'movie' in reviews_for_template[0] and isinstance(reviews_for_template[0]['movie'], Movie):
                    print("O primeiro item tem a chave 'movie' e é um objeto Movie!")
                else:
                    print("AVISO: O primeiro item NÃO tem a chave 'movie' ou não é um objeto Movie.")
        else:
            print("reviews_for_template está vazia.")
        print("--- FIM DEBUG ---\n")
        # --- FIM DAS LINHAS DE DEBUG ---

        # Renderiza o template de perfil do usuário
        return self.render('user_profile', 
                            user=logged_in_user, 
                            reviews=reviews_for_template) # Passe a lista já pronta

    #metodo Página de Perfil de OUTRO Usuário (Opcional) ---
    def user_profile_by_id(self, user_id):
        logged_in_user = self.get_logged_in_user()
        if not logged_in_user:
            return self.redirect(f'/login?next=/users/{user_id}/profile')

        target_user = self.user_service.get_by_id(user_id)
        if not target_user:
            return HTTPError(404, "Usuário não encontrado.") 

        # Pega as avaliações para o usuário alvo.
        # Assim como em user_profile, o retorno já está no formato correto.
        reviews_for_template = self.avaliacao_service.get_all_avaliacoes_by_user_id(target_user.id)
        
        # --- LINHAS DE DEBUG: ADICIONE ESTAS 4 LINHAS TAMBÉM AQUI ---
        print("\n--- DEBUG: reviews_for_template no user_profile_by_id ---")
        print(f"Tipo de reviews_for_template: {type(reviews_for_template)}")
        if reviews_for_template:
            print(f"Tipo do primeiro item: {type(reviews_for_template[0])}")
            if isinstance(reviews_for_template[0], dict):
                print(f"Chaves do primeiro item: {reviews_for_template[0].keys()}")
                if 'movie' in reviews_for_template[0] and isinstance(reviews_for_template[0]['movie'], Movie):
                    print("O primeiro item tem a chave 'movie' e é um objeto Movie!")
                else:
                    print("AVISO: O primeiro item NÃO tem a chave 'movie' ou não é um objeto Movie.")
        else:
            print("reviews_for_template está vazia.")
        print("--- FIM DEBUG ---\n")
        # --- FIM DAS LINHAS DE DEBUG ---

        return self.render('user_profile', 
                            user=target_user, 
                            reviews=reviews_for_template)


user_routes = Bottle()
user_controller = UserController(user_routes)