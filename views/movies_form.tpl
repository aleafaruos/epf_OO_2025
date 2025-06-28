%rebase('layout', title='Adicionar/Editar Filme')

<section class="form-section">
    <div class="section-header">
        <h1 class="section-title">
            <i class="fas fa-{{'edit' if movie else 'plus-circle'}}"></i> 
            {{'Editar Filme' if movie else 'Adicionar Novo Filme'}}
        </h1>
    </div>

    <form action="{{action}}" method="post" class="styled-form">
        <div class="form-group">
            <label for="name">Título:</label>
            <input type="text" id="name" name="name" value="{{movie.name if movie else ''}}" required>
        </div>

        <div class="form-group">
            <label for="ano">Ano:</label>
            <input type="number" id="ano" name="ano" value="{{movie.ano if movie else ''}}" required>
        </div>
        <div class="form-group">
            <label for="poster">URL do Pôster:</label>
            <input type="url" id="poster" name="poster" value="{{movie.poster if defined('movie') and movie else ''}}">
            <small>Ex: https://image.tmdb.org/t/p/w500/c7W7Qf4k7yP7yQ8l8Q8z0L0j2k.jpg</small>
        </div>
        <div class="form-group">
            <label for="resumo">Resumo:</label>
            <textarea id="resumo" name="resumo" rows="5">{{movie.resumo if defined('movie') and movie else ''}}</textarea>
        </div>
        <div class="form-group">
            <label for="avaliacao_media">Avaliação Média (0.0 a 10.0):</label>
            <input type="number" id="avaliacao_media" name="avaliacao_media" step="0.1" min="0" max="10" value="{{'%.1f' % movie.avaliacao_media if defined('movie') and movie else '0.0'}}">
        </div>
        <div class="form-group">
            <label for="numero_votos">Número de Votos:</label>
            <input type="number" id="numero_votos" name="numero_votos" min="0" value="{{movie.numero_votos if defined('movie') and movie else '0'}}">
        </div>
         <div class="form-group">
            <label for="popularidade">Popularidade (0.00 a N):</label>
            <input type="number" id="popularidade" name="popularidade" step="0.01" min="0" value="{{'%.2f' % movie.popularidade if defined('movie') and movie else '0.00'}}">
        </div>

        
        <div class="form-actions">
            <button type="submit" class="btn btn-success">Salvar</button>
            <a href="/movies" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</section>