import json
import os
from dataclasses import dataclass, asdict
from typing import List

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class Movie:
    def __init__(self, id, name, ano, diretor):
        self.id = id
        self.name = name
        self.ano = ano 
        self.diretor = diretor


    def __repr__(self):
        return (f"movie(id={self.id}, name='{self.name}', ano='{self.ano}', "
                f"diretor='{self.diretor}'")


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ano': self.ano,
            'diretor': self.diretor
        }


    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            name=data['name'],
            ano=data['ano'],
            diretor=data['diretor']
        )


class movieModel:
    FILE_PATH = os.path.join(DATA_DIR, 'movies.json')

    def __init__(self):
        self.movies = self._load()


    def _load(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Movie(**item) for item in data]


    def _save(self):
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