%rebase('layout', title='Avaliar Filme')

<section class="form-section">
    <div class="form-container">
        <h1 class="form-title">Avaliar Filme: {{movie.name}}</h1>

        % if defined('error_message') and error_message:
        <p class="error-message">{{error_message}}</p>
        % end

        <div style="text-align: center; margin-bottom: 20px;">
            %if movie.poster:
                <img src="{{movie.poster}}" alt="Pôster de {{movie.name}}" style="max-width: 200px; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            %else:
                <img src="/static/images/no_poster.png" alt="Pôster não disponível" style="max-width: 200px; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            %end
        </div>

        <p class="movie-summary">{{movie.resumo}}</p>

        <form action="/filmes/{{movie.id}}/avaliar" method="POST" class="styled-form">
            <div class="form-group">
                <label for="avaliacao">Sua Avaliação (0.0 a 10.0):</label>
                <input type="number" id="avaliacao" name="avaliacao" step="0.1" min="0" max="10" 
                       value="{{movie.avaliacao_media if movie.avaliacao_media is not None else '0.0'}}" required>
            </div>
            
            <div class="form-group">
                <label for="comentario">Comentário:</label>
                <textarea id="comentario" name="comentario" rows="5" placeholder="Deixe seu comentário sobre o filme...">{{movie.comentario or ''}}</textarea>
            </div>
            <input type="hidden" name="name" value="{{movie.name}}">
            <input type="hidden" name="ano" value="{{movie.ano}}">
            <input type="hidden" name="poster" value="{{movie.poster or ''}}">
            <input type="hidden" name="resumo" value="{{movie.resumo or ''}}">
            <input type="hidden" name="numero_votos" value="{{movie.numero_votos or 0}}">
            <input type="hidden" name="popularidade" value="{{movie.popularidade or 0.0}}">

            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Salvar Avaliação</button>
                <a href="/movies" class="btn btn-secondary">Cancelar</a>
            </div>
        </form>
    </div>
</section>

<style>
    .movie-summary {
        text-align: center;
        font-size: 1.1em;
        margin: 10px auto 30px;
        max-width: 600px;
        line-height: 1.5;
        color: #444;
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
