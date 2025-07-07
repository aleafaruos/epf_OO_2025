import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

        
class Movie:
    def __init__(self, id, name, ano, poster=None, resumo:str='', avaliacao_media:float=0.0, numero_votos:int=0, popularidade:float=0.0):
        self.id = id
        self.name = name
        self.ano = ano 
        self.poster = poster
        self.resumo = resumo
        self.avaliacao_media = avaliacao_media
        self.numero_votos = numero_votos
        self.popularidade = popularidade

    def __repr__(self):
        return f"Movie(id={self.id}, name='{self.name}', ano='{self.ano}')"

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        """
        ✅ CÓDIGO CORRIGIDO SEM ERRO DE SINTAXE
        """
        # Pega o caminho do pôster dos dados da API.
        poster_path = data.get('poster_path')
        
        full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ''
        
        return cls(
            id=data.get('id'),
            name=data.get('title'),
            ano=data.get('release_date'),
            poster=full_poster_url,  
            resumo=data.get('overview', ''),
            avaliacao_media=float(data.get('vote_average', 0.0)),
            numero_votos=int(data.get('vote_count', 0)),
            popularidade=float(data.get('popularity', 0.0))
        )

class movieModel:
    FILE_PATH = os.path.join(DATA_DIR, 'movies.json')

    def __init__(self):
        self.movies = self._load()

    def _load(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        try:
            with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
                raw_movies_data = json.load(f)
                return [Movie.from_dict(item) for item in raw_movies_data]
        except (json.JSONDecodeError, Exception):
            return []

    def _save(self):
        os.makedirs(os.path.dirname(self.FILE_PATH), exist_ok=True)
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([m.to_dict() for m in self.movies], f, indent=4, ensure_ascii=False)

    def get_all(self):
        return self.movies

    def get_by_id(self, movie_id: int):
        return next((m for m in self.movies if m.id == movie_id), None)

    def add_movie(self, movie: Movie):
        self.movies.append(movie)
        self._save()

    def update_movie(self, updated_movie: Movie):
        for i, movie in enumerate(self.movies):
            if movie.id == updated_movie.id:
                self.movies[i] = updated_movie
                self._save()
                break

    def delete_movie(self, movie_id: int):
        self.movies = [m for m in self.movies if m.id != movie_id]
        self._save()