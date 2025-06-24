from bottle import Bottle, request, redirect
from .base_controller import BaseController
from services.user_service import UserService

class UserController(BaseController):
    def __init__(self, app):
        super().__init__(app)

        self.setup_routes()
        self.user_service = UserService()


    # Rotas User
    def setup_routes(self):
        self.app.route('/users', method='GET', callback=self.list_users)
        self.app.route('/users/add', method=['GET', 'POST'], callback=self.add_user)
        self.app.route('/users/edit/<user_id:int>', method=['GET', 'POST'], callback=self.edit_user)
        self.app.route('/users/delete/<user_id:int>', method='POST', callback=self.delete_user)
        self.app.route('/login', method='GET', callback=self.login_form)
        self.app.route('/login', method='POST', callback=self.do_login)


    def list_users(self):
        users = self.user_service.get_all()
        return self.render('users', users=users)


    def add_user(self):
        if request.method == 'GET':
            return self.render('user_form', user=None, action="/users/add")
        else:
            # POST - salvar usuário
            self.user_service.save()
            self.redirect('/users')


    def edit_user(self, user_id):
        user = self.user_service.get_by_id(user_id)
        if not user:
            return "Usuário não encontrado"

        if request.method == 'GET':
            return self.render('user_form', user=user, action=f"/users/edit/{user_id}")
        else:
            # POST - salvar edição
            self.user_service.edit_user(user)
            self.redirect('/users')


    def delete_user(self, user_id):
        self.user_service.delete_user(user_id)
        self.redirect('/users')

    def login_form(self):
        # Passa email vazio e mensagem de erro vazia para o template inicialmente
        return self.render('login_form', email='', error_message='')

    def do_login(self):
        email = request.forms.get('email')
        raw_password = request.forms.get('senha')

        user = self.user_service.check_credentials(email, raw_password)

        if user:
            # Login bem-sucedido!
            # FUTURAMENTE: Aqui você configuraria uma sessão para o usuário (cookies, etc.)
            print(f"Usuário {user.name} logado com sucesso!")
            self.redirect('/users') # Redireciona para a lista de usuários ou dashboard

        else:
            # Login falhou
            error = "Email ou senha inválidos."
            # Renderiza o formulário novamente, passando o email digitado e a mensagem de erro
            return self.render('login_form', email=email, error_message=error)

user_routes = Bottle()
user_controller = UserController(user_routes)
