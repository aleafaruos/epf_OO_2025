import json
import os
from models.movie import Movie, movieModel # ESSENCIAL: MovieModel precisa estar aqui
from typing import List, Optional
from bottle import request # Mantenha se ainda usa em outros métodos, como save/edit

class movieService:
    def __init__(self):
        self.movie_model = movieModel()

    def get_all(self, termo_busca: str = None):
        movies = self.movie_model.get_all() # Pega todos os filmes do modelo
        
        if termo_busca:
            termo_lower = termo_busca.lower()
            return [
                movie for movie in movies 
                if termo_lower in movie.name.lower() or 
                   (movie.resumo and termo_lower in movie.resumo.lower()) # Adicionado filtro por resumo também
            ]
        else:
            return movies

    def save(self):
        # Este método 'save' parece ser para adicionar filmes criados *manualmente* via formulário.
        # A lógica de geração de ID aqui pode conflitar com IDs da API se você tentar salvar
        # um filme local com um ID que coincide com um da API.
        # Para filmes vindo da API, usaremos 'save_or_get_movie'.
        
        last_id = max([m.id for m in self.movie_model.get_all()], default=0)
        new_id = last_id + 1 
        
        name = request.forms.get('name')
        ano = request.forms.get('ano')
        poster = request.forms.get('poster')
        resumo = request.forms.get('resumo')
        
        # --- LINHA CORRIGIDA: DEFINIÇÃO DE avaliacao_media NO MÉTODO save() ---
        avaliacao_media = float(request.forms.get('avaliacao_media', '0.0').replace(',', '.'))
        # --- FIM DA LINHA CORRIGIDA ---

        numero_votos = int(request.forms.get('numero_votos', 0))
        popularidade = float(request.forms.get('popularidade', 0.0).replace(',', '.'))

        # Campos adicionais que o Movie pode ter, se não forem preenchidos pelo formulário,
        # podem ser definidos com valores padrão ou None.
        # O ideal é que o formulário de adição manual preencha tudo que o Movie espera,
        # ou que o construtor do Movie lide com None para esses campos opcionais.
        movie = Movie(
            id=new_id, 
            name=name, 
            ano=ano, 
            poster=poster, 
            resumo=resumo, 
            avaliacao_media=avaliacao_media, # Agora estará definida!
            numero_votos=numero_votos, 
            popularidade=popularidade,
            # Campos que não vêm do seu formulário de adição manual, mas existem no Movie
            original_name=name, # Assumindo que o nome original é o mesmo para filmes manuais
            release_date=f"{ano}-01-01", # Formato de data fictício
            genre_ids=[], # Sem genres para filmes manuais, por padrão
            overview=resumo, # overview e resumo são o mesmo neste contexto
            poster_path=poster, # poster_path é o mesmo que poster
            backdrop_path="", # Sem backdrop para filmes manuais
            comentario="" # Comentário inicial vazio
        )
        self.movie_model.add_movie(movie)


    def get_by_id(self, movie_id):
        # Este método busca apenas no seu JSON local.
        return self.movie_model.get_by_id(movie_id)
    
    # --- MÉTODO save_or_get_movie (ATIVADO E AJUSTADO) ---
    def save_or_get_movie(self, movie_data: dict) -> Movie:
        """
        Verifica se um filme já existe localmente pelo ID.
        Se não existir, cria um novo objeto Movie a partir dos dados da API
        e o salva no movies.json.
        Retorna o objeto Movie (existente ou recém-salvo).
        """
        movie_id = movie_data.get('id') # Usar .get() para segurança, embora IDs de filme da API sejam obrigatórios
        if not movie_id:
            raise ValueError("ID do filme é obrigatório para save_or_get_movie.")

        existing_movie = self.get_by_id(movie_id) # Busca no seu JSON local usando o get_by_id existente

        if existing_movie:
            # O filme já está salvo localmente, apenas retorne-o.
            return existing_movie
        else:
            # O filme não está no seu JSON local, então vamos criá-lo
            # e salvá-lo. Mapeamos os campos da API para seu modelo Movie.
            new_movie = Movie(
                id=movie_data.get('id'),
                name=movie_data.get('title'), # 'name' no seu Movie é 'title' na API
                original_name=movie_data.get('original_title', movie_data.get('title')),
                # 'ano' no seu Movie é parte de 'release_date' na API
                ano=movie_data.get('release_date', 'N/A')[:4], # Pega apenas o ano
                # 'poster' no seu Movie é o caminho completo, 'poster_path' na API é só o final
                poster=f"https://image.tmdb.org/t/p/w500/{movie_data.get('poster_path')}" if movie_data.get('poster_path') else '',
                resumo=movie_data.get('overview', ''),
                avaliacao_media=movie_data.get('vote_average', 0.0),
                numero_votos=movie_data.get('vote_count', 0),
                popularidade=movie_data.get('popularity', 0.0),
                comentario="", # Comentário inicia vazio
                release_date=movie_data.get('release_date', 'N/A'),
                genre_ids=movie_data.get('genre_ids', []),
                overview=movie_data.get('overview', ''),
                poster_path=movie_data.get('poster_path'), 
                backdrop_path=movie_data.get('backdrop_path'),
                vote_average=movie_data.get('vote_average', 0.0),
                vote_count=movie_data.get('vote_count', 0)
            )
            self.movie_model.add_movie(new_movie) # Salva o novo filme no movies.json
            return new_movie

    def edit_movie(self, movie_id):
        movie = self.get_by_id(movie_id) 
        if not movie:
            return None 

        name = request.forms.get('name')
        ano = request.forms.get('ano')
        poster = request.forms.get('poster')
        resumo = request.forms.get('resumo')
        
        # --- LINHA CORRIGIDA: DEFINIÇÃO DE avaliacao_media NO MÉTODO edit_movie() ---
        avaliacao_media = float(request.forms.get('avaliacao_media', '0.0').replace(',', '.'))
        # --- FIM DA LINHA CORRIGIDA ---

        numero_votos = int(request.forms.get('numero_votos', 0))
        popularidade = float(request.forms.get('popularidade', 0.0).replace(',', '.'))
        comentario = request.forms.get('comentario', '') 
        
        movie.name = name
        movie.ano = ano
        movie.poster = poster
        movie.resumo = resumo
        movie.avaliacao_media = avaliacao_media 
        movie.numero_votos = numero_votos
        movie.popularidade = popularidade
        movie.comentario = comentario 

        self.movie_model.update_movie(movie)
        return movie 

    # --- MÉTODO update_movie_rating (AGORA COM PRINTS DE DEBUG) ---
    def update_movie_rating(self, movie_id: int, nova_avaliacao: float, comentario: str):
        """
        Atualiza apenas a avaliação média e o comentário de um filme.
        Inclui prints de debug para rastrear o fluxo.
        """
        print(f"DEBUG_SERVICE: Iniciando update_movie_rating para ID: {movie_id}")
        print(f"DEBUG_SERVICE: Nova avaliação recebida: {nova_avaliacao}, Comentário: '{comentario}'")
        try:
            movie = self.get_by_id(movie_id) 
            if not movie:
                print(f"DEBUG_SERVICE: Filme com ID {movie_id} NÃO ENCONTRADO no JSON local.")
                raise ValueError(f"Filme com ID {movie_id} não encontrado para atualizar avaliação.")

            print(f"DEBUG_SERVICE: Filme '{movie.name}' (ID: {movie.id}) encontrado.")
            print(f"DEBUG_SERVICE: Avaliação anterior: {movie.avaliacao_media}, Comentário anterior: '{movie.comentario}'")

            # Atualiza apenas os campos relevantes
            movie.avaliacao_media = nova_avaliacao
            movie.comentario = comentario

            print(f"DEBUG_SERVICE: Campos do filme atualizados em memória. Chamando movie_model.update_movie...")
            self.movie_model.update_movie(movie) 
            print(f"DEBUG_SERVICE: movie_model.update_movie EXECUTADO com sucesso para ID {movie.id}.")
            return True
        except Exception as e:
            # Captura qualquer exceção genérica e a relança com uma mensagem útil.
            print(f"ERRO NO update_movie_rating DO SERVICE: Ocorreu um erro ao atualizar o filme {movie_id}: {e}")
            raise Exception(f"Falha ao salvar avaliação do filme (ID: {movie_id}): {e}")
    # --- FIM MÉTODO update_movie_rating ---


    def delete_movie(self, movie_id):
        self.movie_model.delete_movie(movie_id)