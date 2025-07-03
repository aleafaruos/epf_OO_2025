import json
import os
from dataclasses import dataclass, asdict
from typing import List,Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
MOVIES_FILE = os.path.join(DATA_DIR, 'movies.json')

class Movie:
    # Torne 'comentario' opcional com um valor padrão, como uma string vazia
    def __init__(self, id, name, ano=None, poster=None, resumo:str='', avaliacao_media:float=0.0, numero_votos:int=0, popularidade:float=0.0, comentario:str='',
                 original_name:str=None, release_date:str=None, genre_ids:List[int]=None, overview:str=None, poster_path:str=None, backdrop_path:str=None, vote_average:float=None, vote_count:int=None):
        self.id = id
        self.name = name
        
        # Mapeando campos da API para seus campos existentes (ou usando os da API se vierem)
        self.original_name = original_name if original_name is not None else name # TMDB: original_title
        self.release_date = release_date if release_date is not None else (ano + '-01-01' if ano else 'N/A') # TMDB: release_date
        self.genre_ids = genre_ids if genre_ids is not None else [] # TMDB: genre_ids
        self.overview = overview if overview is not None else resumo # TMDB: overview
        self.poster_path = poster_path if poster_path is not None else poster # TMDB: poster_path
        self.backdrop_path = backdrop_path if backdrop_path is not None else '' # TMDB: backdrop_path (novo campo útil)
        self.vote_average = vote_average if vote_average is not None else avaliacao_media # TMDB: vote_average
        self.vote_count = vote_count if vote_count is not None else numero_votos # TMDB: vote_count
        
        # Seus campos existentes (eles agora serão preenchidos ou mapeados dos campos da API)
        self.ano = ano if ano is not None else (release_date[:4] if release_date else 'N/A') if release_date else 'N/A'
        self.poster = poster if poster is not None else poster_path # Usará poster_path se existir
        self.resumo = resumo if resumo is not None else overview # Usará overview se existir
        self.avaliacao_media = avaliacao_media if avaliacao_media is not None else self.vote_average # Garante que use a que veio ou a mapeada
        self.numero_votos = numero_votos if numero_votos is not None else self.vote_count # Garante que use a que veio ou a mapeada
        self.popularidade = popularidade # Seu campo original
        self.comentario = comentario

    def __repr__(self):
        return (f"Movie(id={self.id}, name='{self.name}', ano='{self.ano}', poster='{self.poster}', "
                f"resumo='{self.resumo[:30]}...',"
                f"avaliacao_media={self.avaliacao_media}, numero_votos={self.numero_votos},"
                f"popularidade={self.popularidade}, comentario='{self.comentario[:30]}...')") # Adicionei o comentário ao repr para depuração

    def to_dict(self):
        # --- INÍCIO DA CORREÇÃO NO to_dict ---
        # Adicione 'comentario' para que ele seja salvo no JSON
        return {
            'id': self.id,
            'name': self.name,
            'ano': self.ano, # Seu campo
            'poster': self.poster, # Seu campo
            'resumo': self.resumo, # Seu campo
            'avaliacao_media': self.avaliacao_media, # Seu campo
            'numero_votos': self.numero_votos, # Seu campo
            'popularidade': self.popularidade, # Seu campo
            'comentario': self.comentario, # Seu campo
            
            # Campos da API para garantir que eles sejam persistidos se estiverem presentes
            'original_name': self.original_name,
            'release_date': self.release_date,
            'genre_ids': self.genre_ids,
            'overview': self.overview,
            'poster_path': self.poster_path,
            'backdrop_path': self.backdrop_path,
            'vote_average': self.vote_average,
            'vote_count': self.vote_count
        }
        # --- FIM DA CORREÇÃO NO to_dict ---


    @classmethod
    def from_dict(cls, data):
        # --- INÍCIO DA CORREÇÃO NO from_dict ---
        # Use .get() para 'comentario' para garantir que ele sempre seja carregado,
        # mesmo se não existir em entradas antigas no JSON.
       return cls(
            id=data['id'],
            name=data['name'],
            ano=data.get('ano'), # Use .get() para campos que podem não existir em JSONs antigos
            poster=data.get('poster'),
            resumo=data.get('resumo', ''),
            avaliacao_media=float(data.get('avaliacao_media', 0.0)),
            numero_votos=int(data.get('numero_votos', 0)),
            popularidade=float(data.get('popularidade', 0.0)),
            comentario=data.get('comentario', ''),
            
            # Carregando campos da API também
            original_name=data.get('original_name'),
            release_date=data.get('release_date'),
            genre_ids=data.get('genre_ids', []),
            overview=data.get('overview'),
            poster_path=data.get('poster_path'),
            backdrop_path=data.get('backdrop_path'),
            vote_average=float(data.get('vote_average', 0.0)),
            vote_count=int(data.get('vote_count', 0))
        )
        # --- FIM DA CORREÇÃO NO from_dict ---


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
            # AQUI ESTÁ O USO DO from_dict. Ele já usará o comentario=data.get('comentario', '')
            return [Movie.from_dict(item) for item in raw_movies_data]
        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON em {self.FILE_PATH}. O arquivo pode estar vazio ou corrompido. Retornando lista vazia.")
            return []
        except Exception as e:
            print(f"Erro inesperado ao carregar filmes de {self.FILE_PATH}: {e}")
            return []

    # O seu código original tinha um bloco 'with open' duplicado aqui. Removi.
    # with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
    #     raw_movies_data = json.load(f)
    #     return [Movie.from_dict(item) for item in raw_movies_data]

    def _save(self):
        os.makedirs(os.path.dirname(self.FILE_PATH), exist_ok=True)
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            # to_dict agora inclui 'comentario', então ele será salvo
            json.dump([u.to_dict() for u in self.movies], f, indent=4, ensure_ascii=False)

    def get_all(self):
        return self.movies

    def get_by_id(self, movie_id: int):
        return next((u for u in self.movies if u.id == movie_id), None)

    def add_movie(self, movie: Movie):
        # Verifica se o filme já existe antes de adicionar para evitar duplicatas
        if not self.get_by_id(movie.id):
            self.movies.append(movie)
            self._save()
            return movie # Retorna o filme adicionado
        return self.get_by_id(movie.id) 

    def update_movie(self, updated_movie: Movie):
        for i, movie in enumerate(self.movies):
            if movie.id == updated_movie.id:
                self.movies[i] = updated_movie
                self._save()
                break

    def delete_movie(self, movie_id: int):
        self.movies = [u for u in self.movies if u.id != movie_id]
        self._save()