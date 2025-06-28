%rebase('layout', title='Filmes')

<section class="movies-section">
    <div class="section-header">
        <h1 class="section-name"><i class="fas fa-movies"></i> Gestão de Filmes</h1>
        <a href="/movies/add" class="btn btn-primary">
            <i class="fas fa-plus"></i> Novo Filme
        </a>
    </div>

    <div class="table-container">
        <table class="styled-table">
            
            <thead>
                <tr>
                    <th>ID</th>       
                    <th>Título</th>
                    <th>Diretor</th>   
                    <th>Ano</th>       
                </tr>
            </thead>

            <tbody>
                % for movie in movies: 
                <tr>
                    <td>{{movie.id}}</td>         
                    <td>{{movie.name}}</td>       
                    <td>{{movie.diretor}}</td>    
                    <td>{{movie.ano}}</td>        
                    
                    <td class="actions">
                        <a href="/movies/edit/{{movie.id}}" class="btn btn-sm btn-edit"> 
                            <i class="fas fa-edit"></i> Editar
                        </a>

                        <form action="/movies/delete/{{movie.id}}" method="post" {# Link de exclusão atualizado para movie.id #}
                              onsubmit="return confirm('Tem certeza?')">
                            <button type="submit" class="btn btn-sm btn-danger">
                                <i class="fas fa-trash-alt"></i> Excluir
                            </button>
                        </form>
                    </td>
                </tr>
                % end
            </tbody>
        </table>
    </div>
</section>