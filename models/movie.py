import json
import os
from dataclasses import dataclass, asdict
from typing import List

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class Movie:
    def __init__(self, id, name, ano, poster,resumo:str='',avaliacao_media:float=0.0,numero_votos:int=0,popularidade:float=0.0 ):
        
        self.id = id
        self.name = name
        self.ano = ano 
        self.poster = poster
        self.resumo = resumo
        self.avaliacao_media=avaliacao_media
        self.numero_votos=numero_votos
        self.popularidade=popularidade



    def __repr__(self):
        return (f"Movie(id={self.id}, name='{self.name}', ano='{self.ano}', poster='{self.poster}', " f"resumo='{self.resumo[:30]}...',"f"avaliacao_media={self.avaliacao_media}, numero_votos={self.numero_votos},"f"popularidade={self.popularidade})")


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ano': self.ano,
            'poster': self.poster,
            'resumo':self.resumo,
            'avaliacao_media':self.avaliacao_media,
            'numero_votos':self.numero_votos,
            'popularidade':self.popularidade

        }


    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            name=data['name'],
            ano=data['ano'],
            poster=data.get('poster', ''),                # CORRIGIDO: de data.get['poster'] para data.get('poster', '')
            resumo=data.get('resumo', ''),                # CORRIGIDO: de data.get['resumo'] para data.get('resumo', '')
            avaliacao_media=data.get('avaliacao_media', 0.0), # CORRIGIDO
            numero_votos=data.get('numero_votos', 0),     # CORRIGIDO
            popularidade=data.get('popularidade', 0.0)
        )


class movieModel:
    FILE_PATH = os.path.join(DATA_DIR, 'movies.json')

    def __init__(self):
        self.movies = self._load()


    def _load(self):
        if not os.path.exists(self.FILE_PATH):
            return [] # Retorna lista vazia se o arquivo não existe

        try:
            with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
                raw_movies_data = json.load(f)
                return [Movie.from_dict(item) for item in raw_movies_data]
        except json.JSONDecodeError: # ADICIONADO: Tratamento para JSON vazio ou corrompido
            print(f"Erro ao decodificar JSON em {self.FILE_PATH}. O arquivo pode estar vazio ou corrompido. Retornando lista vazia.")
            return []
        except Exception as e: # ADICIONADO: Tratamento para outros erros de carregamento
            print(f"Erro inesperado ao carregar filmes de {self.FILE_PATH}: {e}")
            return []
        with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
            raw_movies_data = json.load(f) # Renomeei para evitar conflito com 'data' no loop
        # Use from_dict para carregar, pois ele já tem o .get() para 'poster'
            return [Movie.from_dict(item) for item in raw_movies_data]


    def _save(self):
        os.makedirs(os.path.dirname(self.FILE_PATH), exist_ok=True)
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([u.to_dict() for u in self.movies], f, indent=4, ensure_ascii=False)


    def get_all(self):
        return self.movies


    def get_by_id(self, movie_id: int):
        return next((u for u in self.movies if u.id == movie_id), None)


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
        self.movies = [u for u in self.movies if u.id != movie_id]
        self._save()