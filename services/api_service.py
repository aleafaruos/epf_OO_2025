# services/api_service.py
import requests

class TMDBService:
    def __init__(self):
        self.api_key = '837d294758fed763def26fe173fc765f' # Sua chave de API
        self.base_url = 'https://api.themoviedb.org/3'

    def _make_request(self, endpoint, params=None):
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        params['language'] = 'pt-BR'

        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status() # Lança um erro para status de resposta ruins (4xx ou 5xx)
        return response.json()

    def search_movies(self, query):
        return self._make_request('search/movie', {'query': query}).get('results', [])

    def get_popular_movies(self):
        return self._make_request('movie/popular').get('results', [])

    def get_movie_details(self, movie_id):
        return self._make_request(f'movie/{movie_id}')