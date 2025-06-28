from bottle import Bottle, request,redirect,response
from .base_controller import BaseController
from services.movie_service import movieService

class movieController(BaseController):
    def __init__(self, app):
        super().__init__(app)

        self.setup_routes()
        self.movie_service = movieService()


    # Rotas movie
    def setup_routes(self):
        self.app.route('/movies', method='GET', callback=self.list_movies)
        self.app.route('/movies/add', method=['GET', 'POST'], callback=self.add_movie)
        self.app.route('/movies/edit/<movie_id:int>', method=['GET', 'POST'], callback=self.edit_movie)
        self.app.route('/movies/delete/<movie_id:int>', method='POST', callback=self.delete_movie)


    def list_movies(self):
        movies = self.movie_service.get_all()
        return self.render('movies', movies=movies)


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
            return "Usuário não encontrado"

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