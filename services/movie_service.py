import json
import os
from models.movie import Movie, movieModel # ESSENCIAL: MovieModel precisa estar aqui
from typing import List, Optional, Tuple # Importe Tuple
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

        movie = Movie(
            id=new_id,
            name=name,
            ano=ano,
            poster=poster,
            resumo=resumo,
            avaliacao_media=avaliacao_media,
            numero_votos=numero_votos,
            popularidade=popularidade,
            original_name=name,
            release_date=f"{ano}-01-01",
            genre_ids=[],
            overview=resumo,
            poster_path=poster,
            backdrop_path="",
            comentarios=[] # Inicializado como lista vazia
        )
        self.movie_model.add_movie(movie)


    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        # Este método busca apenas no seu JSON local.
        return self.movie_model.get_by_id(movie_id)

    def save_or_get_movie(self, movie_data: dict) -> Movie:
        """
        Verifica se um filme já existe localmente pelo ID.
        Se não existir, cria um novo objeto Movie a partir dos dados da API
        e o salva no movies.json.
        Retorna o objeto Movie (existente ou recém-salvo).
        """
        movie_id = movie_data.get('id')
        if not movie_id:
            raise ValueError("ID do filme é obrigatório para save_or_get_movie.")

        existing_movie = self.get_by_id(movie_id)

        if existing_movie:
            return existing_movie
        else:
            new_movie = Movie(
                id=movie_data.get('id'),
                name=movie_data.get('title'),
                original_name=movie_data.get('original_title', movie_data.get('title')),
                ano=movie_data.get('release_date', 'N/A')[:4],
                poster=f"https://image.tmdb.org/t/p/w500/{movie_data.get('poster_path')}" if movie_data.get('poster_path') else '',
                resumo=movie_data.get('overview', ''),
                avaliacao_media=movie_data.get('vote_average', 0.0), # Valor inicial da API
                numero_votos=movie_data.get('vote_count', 0), # Valor inicial da API
                popularidade=movie_data.get('popularity', 0.0),
                comentarios=[], # Inicializado como lista vazia
                release_date=movie_data.get('release_date', 'N/A'),
                genre_ids=movie_data.get('genre_ids', []),
                overview=movie_data.get('overview', ''),
                poster_path=movie_data.get('poster_path'),
                backdrop_path=movie_data.get('backdrop_path'),
                vote_average=movie_data.get('vote_average', 0.0),
                vote_count=movie_data.get('vote_count', 0)
            )
            self.movie_model.add_movie(new_movie)
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

        movie.name = name
        movie.ano = ano
        movie.poster = poster
        movie.resumo = resumo
        movie.avaliacao_media = avaliacao_media
        movie.numero_votos = numero_votos
        movie.popularidade = popularidade
        # Não há mais 'movie.comentario' aqui

        self.movie_model.update_movie(movie)
        return movie

    # --- MÉTODO update_movie_rating - CORRIGIDO E ATUALIZADO ---
    def update_movie_rating(self, movie_id: int, user_id: int, nova_avaliacao: float, comentario_data: Optional[Tuple[str, str]]):
        """
        Atualiza a avaliação e adiciona/atualiza um comentário para um filme.
        :param movie_id: ID do filme.
        :param nova_avaliacao: A nova nota numérica dada pelo usuário.
        :param comentario_data: Uma tupla (texto do comentário, nome do usuário) ou None.
        """
        movie = self.get_by_id(movie_id)
        if not movie:
            print(f"Erro (movieService): Filme com ID {movie_id} não encontrado para avaliação.")
            return False

        # Certifica-se de que 'comentarios' é uma lista
        if not hasattr(movie, 'comentarios') or not isinstance(movie.comentarios, list):
            movie.comentarios = []

        # Extrai os dados do comentário (se houver)
        comentario_texto = None
        user_name = None
        if comentario_data:
            comentario_texto, user_name = comentario_data
            
        # Para fins de demonstração, vamos usar um user_id temporário se o logged_in_user real não estiver disponível aqui.
        # Em um sistema real, o user_id viria do `logged_in_user` do controller.
        # Como o `movie_service` não tem acesso direto ao `request` ou ao `logged_in_user`,
        # o `movie_controller` deve passar o `user_id` (e `user_name`) explictamente.
        # Por enquanto, vamos simular que o `user_id` é o `logged_in_user.id` vindo do controller.
        # O `user_name` já está vindo na tupla `comentario_data`.

        # ASSUMIR: `movie_controller` deve passar `logged_in_user.id` para este método.
        # Vou adicionar um placeholder aqui para você lembrar de passar o ID do usuário.
        # Por exemplo: `self.movie_service.update_movie_rating(movie.id, logged_in_user.id, nova_avaliacao, comentario_data)`
        # E aqui no service: `def update_movie_rating(self, movie_id: int, user_id: int, nova_avaliacao: float, comentario_data: Optional[Tuple[str, str]])`
        
        # Para fins de teste *agora*, vamos usar um ID de usuário fixo temporário ou obter do logged_in_user (se passado)
        # Se você não passou o user_id do controller, isso precisará ser ajustado.
        # POR FAVOR, CERTIFIQUE-SE DE QUE O CONTROLLER ESTÁ PASSANDO O user_id!
        # Por exemplo, modifique a chamada no controller para:
        # self.movie_service.update_movie_rating(movie.id, logged_in_user.id, nova_avaliacao, comentario_data)
        # E adicione `user_id: int,` na assinatura deste método `update_movie_rating`.

        # Placeholder temporário, se o user_id não estiver vindo do controller
        # Se você já passou o logged_in_user.id do controller, remova esta linha:
        # user_id = 1 # ID de usuário temporário para fins de teste se não vier do controller

        # Para que este método funcione, ele *precisa* do user_id do usuário que está avaliando.
        # No `movie_controller.py`, a linha deve ser:
        # `self.movie_service.update_movie_rating(movie.id, logged_in_user.id, nova_avaliacao, comentario_data)`
        # E a assinatura deste método aqui deve ser:
        # `def update_movie_rating(self, movie_id: int, user_id: int, nova_avaliacao: float, comentario_data: Optional[Tuple[str, str]]):`

        # Vamos assumir que `user_id` virá como um parâmetro para este método,
        # e `user_name` virá dentro de `comentario_data`.
        # Para que o seu código atual no controller funcione, precisamos do `logged_in_user.id` lá.
        # Então, volte no `movie_controller.py` na linha:
        # `self.movie_service.update_movie_rating(movie.id, nova_avaliacao, comentario_data)`
        # e mude para:
        # `self.movie_service.update_movie_rating(movie.id, logged_in_user.id, nova_avaliacao, comentario_data)`
        # Depois, ajuste a assinatura deste método `update_movie_rating` aqui para incluir `user_id`.

        # Assinatura corrigida para o `movie_service.py`:
        # def update_movie_rating(self, movie_id: int, user_id: int, nova_avaliacao: float, comentario_data: Optional[Tuple[str, str]]):

        # Para o propósito da correção AGORA, vou adicionar o `user_id` como um parâmetro
        # e assumir que ele vem do controller.
        # POR FAVOR, MANTENHA A ATENÇÃO NESSA INSTRUÇÃO PARA O CONTROLLER!
        
        # O `user_id` PRECISA vir do controller. Eu adicionei-o na assinatura abaixo.

        # Verifica se o usuário já tem um comentário/avaliação existente para este filme
        found_comment_index = -1
        if user_name: # Apenas busca se houver um user_name para associar
            for i, c in enumerate(movie.comentarios):
                # Usar o user_name para identificar o comentário, já que user_id pode não estar sempre presente
                # Se `user_id` for garantido, é melhor usar `c.get('user_id') == user_id`
                if c.get('user_name') == user_name:
                    found_comment_index = i
                    break

        # Prepara o novo/atualizado comentário
        # O comentário deve ser adicionado APENAS se `comentario_texto` não for vazio,
        # OU se a avaliação estiver sendo atualizada para um usuário existente.
        
        # Garante que `user_name` não é None se `comentario_data` não for None
        # O `user_name` virá de `logged_in_user.name` no controller.
        # Se `comentario_data` for None, não haverá `comentario_texto` nem `user_name` novos.
        
        if comentario_texto or (found_comment_index != -1): # Se houver texto ou se for uma atualização
            comentario_entry = {
                'user_id': user_id, # Este `user_id` deve vir do controller!
                'user_name': user_name, # Este `user_name` deve vir de `comentario_data` (do controller)
                'avaliacao': nova_avaliacao,
                'comentario_texto': comentario_texto.strip(),
                'timestamp': '2025-07-03T19:00:00Z' # Exemplo de timestamp
            }

            if found_comment_index != -1:
                # Atualiza o comentário existente do usuário
                movie.comentarios[found_comment_index] = comentario_entry
            else:
                # Adiciona um novo comentário à lista, mas APENAS se o `comentario_texto` não for vazio
                # ou se o usuário estiver dando uma avaliação pela primeira vez.
                # Se for apenas uma avaliação sem texto, e ele já tem um, atualiza.
                # Se for uma nova avaliação sem texto, ainda é válido adicionar.
                movie.comentarios.append(comentario_entry)
        else:
            # Se `comentario_data` for None (sem texto de comentário novo), e não houver um comentário existente
            # do usuário para atualizar, não adicionamos um novo objeto de comentário vazio.
            pass # Nenhuma ação para o comentário, mas a avaliação geral será recalculada.


        # Recalcula avaliacao_media e numero_votos com base em TODOS os comentários
        total_avaliacoes = 0
        soma_avaliacoes = 0

        if movie.comentarios:
            for c in movie.comentarios:
                soma_avaliacoes += c['avaliacao']
                total_avaliacoes += 1

            movie.avaliacao_media = soma_avaliacoes / total_avaliacoes
            movie.numero_votos = total_avaliacoes
        else:
            # Se não houver comentários (após a remoção, por exemplo), volta para os valores TMDB originais ou zero
            # Se movie.vote_average/vote_count vierem de uma API externa, use-os. Caso contrário, defina 0.0/0.
            movie.avaliacao_media = float(movie.vote_average) if movie.vote_average is not None else 0.0
            movie.numero_votos = int(movie.vote_count) if movie.vote_count is not None else 0

        self.movie_model.update_movie(movie)
        return True
    # --- FIM MÉTODO update_movie_rating ---


    def delete_movie(self, movie_id):
        self.movie_model.delete_movie(movie_id)