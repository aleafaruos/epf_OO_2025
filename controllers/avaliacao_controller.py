from bottle import Bottle, request, redirect
from .base_controller import BaseController
from services.avaliacao_service import AvaliacaoService

class AvaliacaoController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.avaliacao_service = AvaliacaoService()
        self.setup_routes()

    def setup_routes(self):
        self.app.route('/avaliacoes/add', method='POST', callback=self.add_avaliacao)

    def add_avaliacao(self):
        self.avaliacao_service.save()
        id_filme = request.forms.get('id_filme')
        if id_filme:
            return self.redirect(f'/movies/{id_filme}')
        else:
            return self.redirect('/movies')

avaliacao_routes = Bottle()
avaliacao_controller = AvaliacaoController(avaliacao_routes)