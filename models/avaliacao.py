# models/avaliacao.py
import json
import os
from datetime import datetime # Importe datetime para usar timestamps

# Diretório base para dados
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
# Caminho para o arquivo de dados dos filmes
MOVIE_DATA_FILE = os.path.join(DATA_DIR, 'movies.json')

class Avaliacao:
    # A classe Avaliacao representa um único comentário/avaliação
    def __init__(self, user_id, user_name, avaliacao, comentario_texto, timestamp=None):
        self.user_id = user_id
        self.user_name = user_name
        self.avaliacao = avaliacao # Este é o valor da nota (ex: 9.0)
        self.comentario_texto = comentario_texto if comentario_texto is not None else ""
        self.timestamp = timestamp if timestamp else datetime.now().isoformat()

    def __repr__(self):
        return f"Avaliacao(user_id={self.user_id}, user_name='{self.user_name}', avaliacao={self.avaliacao}, comentario_texto='{self.comentario_texto}', timestamp='{self.timestamp}')"

    def to_dict(self):
        # Converte o objeto Avaliacao para um dicionário, no formato esperado pelo JSON
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'avaliacao': self.avaliacao,
            'comentario_texto': self.comentario_texto,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        # Cria um objeto Avaliacao a partir de um dicionário (geralmente lido do JSON)
        return cls(
            user_id=data['user_id'],
            user_name=data['user_name'],
            avaliacao=data['avaliacao'],
            comentario_texto=data.get('comentario_texto', ''),
            timestamp=data.get('timestamp')
        )


class avaliacaoModel:
    # Este modelo agora interage DIRETAMENTE com o movies.json para gerenciar avaliações
    def __init__(self):
        self.movies_file_path = MOVIE_DATA_FILE

    def _load_movies_data(self):
        # Carrega o JSON dos filmes
        if not os.path.exists(self.movies_file_path):
            return []
        try:
            with open(self.movies_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Erro ao carregar movies.json em avaliacaoModel: {e}")
            return []

    def _save_movies_data(self, data):
        # Salva o JSON dos filmes
        with open(self.movies_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get_all_avaliacoes_from_movies(self):
        # Retorna uma lista de dicionários, onde cada item contém um objeto Avaliacao
        # e informações básicas do filme ao qual a avaliação pertence.
        all_movies_data = self._load_movies_data()
        all_avaliacoes_com_detalhes_filme = []

        for movie_data in all_movies_data:
            movie_id = movie_data.get('id')
            movie_name = movie_data.get('name')
            movie_poster = movie_data.get('poster')
            movie_ano = movie_data.get('ano')

            for comment_data in movie_data.get('comentarios', []):
                try:
                    avaliacao_obj = Avaliacao.from_dict(comment_data)
                    all_avaliacoes_com_detalhes_filme.append({
                        'avaliacao': avaliacao_obj,
                        'movie_id': movie_id,
                        'movie_name': movie_name,
                        'movie_poster': movie_poster,
                        'movie_ano': movie_ano
                    })
                except KeyError as e:
                    print(f"Erro ao carregar avaliação do filme {movie_id}: Chave ausente - {e}. Dados: {comment_data}")
                except Exception as e:
                    print(f"Erro inesperado ao processar avaliação do filme {movie_id}: {e}. Dados: {comment_data}")
        return all_avaliacoes_com_detalhes_filme

    def add_avaliacao_to_movie(self, movie_id, new_avaliacao: Avaliacao):
        # Adiciona uma nova avaliação a um filme específico.
        all_movies_data = self._load_movies_data()
        found = False
        for movie_data in all_movies_data:
            if movie_data.get('id') == movie_id:
                if 'comentarios' not in movie_data:
                    movie_data['comentarios'] = []
                movie_data['comentarios'].append(new_avaliacao.to_dict())
                found = True
                break
        if found:
            self._save_movies_data(all_movies_data)
            return True
        return False