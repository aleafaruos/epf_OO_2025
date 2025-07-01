from bottle import Bottle, request
from .base_controller import BaseController
from services.avaliacao_service import AvaliacaoService


class AvaliacaoController(BaseController):
    def __init__(self, app):
        super().__init__(app)

        self.setup_routes()
        self.avaliacao_service = AvaliacaoService()


    # Rotas Avaliacao
    def setup_routes(self):
        self.app.route('/avaliacao', method='GET', callback=self.list_avaliacao)
        self.app.route('/avaliacao/add', method=['GET', 'POST'], callback=self.add_avaliacao)
        self.app.route('/avaliacao/edit/<avaliacao_id:int>', method=['GET', 'POST'], callback=self.edit_avaliacao)
        self.app.route('/avaliacao/delete/<avaliacao_id:int>', method='POST', callback=self.delete_avaliacao)

        #self.app.route('/filmes/<filme_id:int>/avaliar', method=['GET', 'POST'], callback=self.avaliar_filme)#

    def list_avaliacao(self):
        avaliacao = self.avaliacao_service.get_all()
        return self.render('avaliacao', avaliacao=avaliacao)
        


    def add_avaliacao(self):
        if request.method == 'GET':
            return self.render('avaliacao_form', avaliacao=None, action="/user"
            ""
            "/add")
        else:
            # POST - salvar usuário
            self.avaliacao_service.save()
            self.redirect('/avaliacao')


    def edit_avaliacao(self, avaliacao_id):
        avaliacao = self.avaliacao_service.get_by_id(avaliacao_id)
        if not avaliacao:
            return "Usuário não encontrado"

        if request.method == 'GET':
            return self.render('avaliacao_form', avaliacao=avaliacao, action=f"/avaliacao/edit/{avaliacao_id}")
        else:
            # POST - salvar edição
            self.avaliacao_service.edit_avaliacao(avaliacao)
            self.redirect('/avaliacao')


    def delete_avaliacao(self, avaliacao_id):
        self.avaliacao_service.delete_avaliacao(avaliacao_id)
        self.redirect('/avaliacao')


avaliacao_routes = Bottle()
avaliacao_controller = AvaliacaoController(avaliacao_routes)