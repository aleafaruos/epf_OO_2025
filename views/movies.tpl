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
                    <th>Pôster</th>       
                    <th>Título</th>
                       
                    <th>Ano</th>
                    <th>resumo</th>
                    <th>avaliação</th>
                    <th>votos</th>
                    <th>popularidade</th>
                    <th>ações</th>       
                </tr>
            </thead>

            <tbody>
                % for movie in movies: 
                <tr>
                    <td>{{movie.id}}</td>
                    <td>
                        %if movie.poster: 
                            <img src="{{movie.poster}}" alt="Pôster de {{movie.name}}" style="width: 80px; height: auto; border-radius: 5px;"> 
                        %else:
                            <img src="/static/images/no_poster.png" alt="Pôster não disponível" style="width: 80px; height: auto; border-radius: 5px;">
                        %end
                    </td>         
                    <td>{{movie.name}}</td>       
                        
                    <td>{{movie.ano}}</td>  
                    <td style="max-width: 250px; text-align: left;"> 
                        %if movie.resumo:
                            <p title="{{movie.resumo}}">
                                {{movie.resumo[:150]}}... 
                            </p>
                        %else:
                            <p>N/A</p>
                        %end
                    </td>
                    <td>{{'%.1f' % movie.avaliacao_media}}/10</td> 
                    <td>{{movie.numero_votos}}</td>           
                    <td>{{'%.2f' % movie.popularidade}}</td>      
                    
                    <td class="actions">
                        <a href="/movies/edit/{{movie.id}}" class="btn btn-sm btn-edit"> 
                            <i class="fas fa-edit"></i> Editar
                        </a>

                        <form action="/movies/delete/{{movie.id}}" method="post" 
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