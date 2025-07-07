import requests
import os

class TMDBService:
    def __init__(self):

        self.api_key = os.getenv('TMDB_API_KEY', '837d294758fed763def26fe173fc765f')
        self.base_url = 'https://api.themoviedb.org/3'
        self.image_base_url = 'https://image.tmdb.org/t/p/w500'

    def _make_request(self, endpoint, params=None):
        if params is None:
            params = {}
        
        params['api_key'] = self.api_key
        params['language'] = 'pt-BR'
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Lança um erro para respostas 4xx/5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro de rede ao aceder a API do TMDb: {e}")
            # Retorna um dicionário vazio ou None para indicar a falha
            return None

    def get_popular_movies(self):
        """Busca a lista de filmes populares."""
        data = self._make_request('/movie/popular')
        return data.get('results', []) if data else []

    def search_movies(self, query):
        """Busca filmes com base numa pesquisa (query)."""
        data = self._make_request('/search/movie', {'query': query})
        return data.get('results', []) if data else []

    def get_movie_details(self, movie_id):
        """Busca os detalhes completos de um filme específico."""
        return self._make_request(f'/movie/{movie_id}')