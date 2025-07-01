%rebase('layout', title='Avaliações')

<section class="avaliacao-section">
    <div class="section-header">
        <h1 class="section-title"><i class="fas fa-avaliacao"></i> Avaliações</h1>
        <a href="/avaliacao/add" class="btn btn-primary">
            <i class="fas fa-plus"></i> Nova avaliação
        </a>
    </div>

    <div class="table-container">
        <table class="styled-table">
            

            <tbody>
                % for u in avaliacao:
                <tr>
                    <td>{{u.id}}</td>
                    <td>{{u.name}}</td>
                    <td><a href="mailto:{{u.email}}">{{u.email}}</a></td>
                    <td>{{u.birthdate}}</td>
                    
                    <td class="actions">
                        <a href="/avaliacao/edit/{{u.id}}" class="btn btn-sm btn-edit">
                            <i class="fas fa-edit"></i> Editar
                        </a>

                        <form action="/avaliacao/delete/{{u.id}}" method="post" 
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