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
            <label for="diretor">Diretor:</label>
            <input type="text" id="diretor" name="diretor" value="{{movie.diretor if movie else ''}}" required>
        </div>
        
        <div class="form-group">
            <label for="ano">Ano:</label>
            <input type="number" id="ano" name="ano" value="{{movie.ano if movie else ''}}" required>
        </div>
        
        <div class="form-actions">
            <button type="submit" class="btn btn-success">Salvar</button>
            <a href="/movies" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</section>