% rebase('layout', title='Todos os Filmes')

<section class="movie-list-section">
    <div class="section-header">
        <h1 class="section-title">Todos os Filmes</h1>
        <a href="/filmes/add" class="btn btn-primary add-movie-btn">
            <i class="fas fa-plus-circle"></i> Adicionar Novo Filme
        </a>
        <form action="/movies" method="get" class="search-form">
            <input type="text" name="termo_busca" placeholder="Buscar filmes..." value="{{termo_busca or ''}}">
            <button type="submit" class="btn btn-search"><i class="fas fa-search"></i></button>
        </form>
    </div>

    % if defined('error_message') and error_message:
        <p class="error-message">{{error_message}}</p>
    % end

    % if movies:
        <div class="movie-grid">
            % for movie_item in movies:
        <div class="movie-card">
                    <a href="/filmes/{{movie_item.id}}">
                        % if movie_item.poster:
                            <img src="{{movie_item.poster}}" alt="{{movie_item.name}}">
                        % else:
                            <img src="/static/images/no_poster.png" alt="Pôster não disponível">
                        % end
                        <h3>{{movie_item.name}} ({{movie_item.ano}})</h3>
                    </a>
                    <div class="card-actions">
                        <a href="/filmes/{{movie_item.id}}/avaliar" class="btn btn-info">Avaliar</a>
                        <a href="/filmes/{{movie_item.id}}/edit" class="btn btn-warning">Editar</a>
                        <a href="/filmes/{{movie_item.id}}/delete" class="btn btn-danger">Excluir</a>
                    </div>
                </div>
            % end
        </div>
    % else:
        <p class="no-movies-found">Nenhum filme encontrado.</p>
    % end
</section>

<style>
    /* Adicione ou referencie seus estilos CSS para a lista de filmes aqui */
    .movie-list-section {
        padding: 20px;
        max-width: 1200px;
        margin: 20px auto;
        background-color: #f8f8f8;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0,0,0,0.05);
    }
    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
        flex-wrap: wrap;
    }
    .section-title {
        color: #333;
        font-size: 2em;
        margin: 0;
    }
    .add-movie-btn {
        background-color: #28a745;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        text-decoration: none;
        font-size: 1em;
    }
    .search-form {
        display: flex;
        gap: 5px;
    }
    .search-form input {
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    .btn-search {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 5px;
        cursor: pointer;
    }
    .movie-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 25px;
        padding: 10px;
    }
    .movie-card {
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        overflow: hidden;
        text-align: center;
        padding-bottom: 15px;
        transition: transform 0.2s ease-in-out;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .movie-card:hover {
        transform: translateY(-5px);
    }
    .movie-card img {
        max-width: 100%;
        height: 300px; /* Altura fixa para pôsteres */
        object-fit: cover; /* Garante que a imagem preencha o espaço sem distorcer */
        display: block;
        margin-bottom: 10px;
    }
    .movie-card h3 {
        font-size: 1.1em;
        color: #333;
        margin: 10px 10px 15px;
        min-height: 50px; /* Garante que os títulos com 1 ou 2 linhas ocupem o mesmo espaço */
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .movie-card a {
        text-decoration: none;
    }
    .card-actions {
        margin-top: auto; /* Empurra os botões para baixo */
        display: flex;
        justify-content: space-around;
        padding: 0 10px;
    }
    .card-actions .btn {
        flex-grow: 1;
        margin: 0 5px;
        padding: 8px 10px;
        font-size: 0.9em;
    }
    .btn-info { background-color: #17a2b8; color: white; }
    .btn-warning { background-color: #ffc107; color: #333; }
    .btn-danger { background-color: #dc3545; color: white; }
    .no-movies-found {
        text-align: center;
        margin-top: 50px;
        font-size: 1.2em;
        color: #666;
    }
    .error-message {
        color: red;
        background-color: #ffe0e0;
        border: 1px solid red;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 5px;
        text-align: center;
    }
</style>