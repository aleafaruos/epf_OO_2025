from bottle import request
from models.movie import movieModel, Movie

class movieService:
    def __init__(self):
        self.movie_model = movieModel()


    def get_all(self, termo_busca: str = None):#tive de modificar aqui também pq tava bugado
        movies = self.movie_model.get_all() # Pega todos os filmes do modelo
        
        if termo_busca:
            # Se um termo de busca for fornecido, filtra os filmes
            termo_lower = termo_busca.lower()
            return [
                movie for movie in movies 
                if termo_lower in movie.name.lower() or 
                   (movie.resumo and termo_lower in movie.resumo.lower()) # Adicionado filtro por resumo também
            ]
        else:
            # Se não houver termo de busca retorna todos os filmes
            return movies


    def save(self):
        last_id = max([u.id for u in self.movie_model.get_all()], default=0)
        new_id = last_id + 1
        name = request.forms.get('name')
        ano = request.forms.get('ano')
        poster = request.forms.get('poster')
        resumo = request.forms.get('resumo')
        avaliacao_media=request.forms.get('avaliacao_media')
        numero_votos=request.forms.get('numero_votos')
        popularidade=request.forms.get('popularidade')

        movie = Movie(id=new_id, name=name, ano=ano,poster=poster,resumo=resumo, avaliacao_media=avaliacao_media, numero_votos=numero_votos,popularidade=popularidade)
        self.movie_model.add_movie(movie)


    def get_by_id(self, movie_id):
        return self.movie_model.get_by_id(movie_id)


    def edit_movie(self, movie):
        name = request.forms.get('name')
        ano = request.forms.get('ano')

        movie.name = name
        movie.ano = ano

        self.movie_model.update_movie(movie)


    def delete_movie(self, movie_id):
        self.movie_model.delete_movie(movie_id)