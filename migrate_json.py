import json
import os

def migrate_movies_json(file_path='data/movies.json'):
    """
    Atualiza o arquivo movies.json, substituindo "comentario" por "comentarios"
    e garantindo que "comentarios" seja sempre uma lista vazia, se não existir.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            movies_data = json.load(f)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{file_path}' não é um JSON válido.")
        return

    updated_movies = []
    changes_made = False

    for movie in movies_data:
        # Verifica se o campo 'comentario' existe e o remove
        if 'comentario' in movie:
            del movie['comentario']
            changes_made = True
        
        # Garante que o campo 'comentarios' exista e seja uma lista
        if 'comentarios' not in movie:
            movie['comentarios'] = []
            changes_made = True
        elif not isinstance(movie['comentarios'], list):
            # Caso "comentarios" exista mas não seja uma lista (improvável, mas para robustez)
            movie['comentarios'] = []
            changes_made = True
        
        updated_movies.append(movie)

    if changes_made:
        try:
            # Salva os dados atualizados de volta no arquivo
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(updated_movies, f, indent=4, ensure_ascii=False)
            print(f"Migração do arquivo '{file_path}' concluída com sucesso.")
            print("O campo 'comentario' foi removido e 'comentarios' foi garantido como lista vazia.")
        except IOError as e:
            print(f"Erro ao escrever no arquivo '{file_path}': {e}")
    else:
        print(f"Nenhuma alteração necessária no arquivo '{file_path}'. Já está no formato correto.")

if __name__ == "__main__":
    # Caminho para o seu arquivo movies.json
    # Certifique-se de que este caminho esteja correto em relação onde você irá rodar o script
    migrate_movies_json(os.path.join(os.path.dirname(__file__), 'data', 'movies.json'))