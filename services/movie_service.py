from bottle import request
from models.movie import movieModel, Movie

class movieService:
    def __init__(self):
        self.movie_model = movieModel()


    def get_all(self):
        movies = self.movie_model.get_all()
        return movies


    def save(self):
        last_id = max([u.id for u in self.movie_model.get_all()], default=0)
        new_id = last_id + 1
        name = request.forms.get('name')
        ano = request.forms.get('ano')
        diretor = request.forms.get('diretor')

        movie = Movie(id=new_id, name=name, ano=ano, diretor=diretor)
        self.movie_model.add_movie(movie)


    def get_by_id(self, movie_id):
        return self.movie_model.get_by_id(movie_id)


    def edit_movie(self, movie):
        name = request.forms.get('name')
        ano = request.forms.get('ano')
        diretor = request.forms.get('diretor')

        movie.name = name
        movie.ano = ano
        movie.diretor = diretor

        self.movie_model.update_movie(movie)


    def delete_movie(self, movie_id):
        self.movie_model.delete_movie(movie_id)