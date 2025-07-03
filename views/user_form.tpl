<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meu App de Filmes</title>
</head>
<body>
    <header>
        <nav>
            <a href="/">Home</a> |
            <a href="/movies">Filmes</a> |
            % if user:
                Olá, {{user.name}}! <a href="/profile">Meu Perfil</a> | <a href="/logout">Sair</a>
            % else:
                <a href="/login">Login</a>
            % end
        </nav>
        <hr>
    </header>
    <main>
    
    <h1>Perfil de {{user.name}}</h1>
    <p>Email: {{user.email}}</p>

    <h2>Minhas Avaliações</h2>
    % if reviews:
    <ul>
    % for item in reviews:
        <li>
            {# Acessando os atributos do OBJETO Movie dentro da chave 'movie' de 'item' #}
            <strong>Filme:</strong> <a href="/filmes/{{item.movie.id}}/avaliar">{{item.movie.name}} ({{item.movie.ano}})</a> <br>
            {# Acessando os atributos do OBJETO Avaliacao dentro da chave 'review' de 'item' #}
            <strong>Nota:</strong> {{item.review.avaliacao}} <br>
            <strong>Comentário:</strong> {{item.review.comentario_texto}}
            {# Acessando o poster do OBJETO Movie #}
            % if item.movie.poster:
                <br><img src="{{item.movie.poster}}" alt="Poster de {{item.movie.name}}" style="width: 100px; height: auto;">
            % end
            {# Opcional: Adicionar o nome do usuário que fez a avaliação e o timestamp #}
            <p style="font-size: 0.8em; color: #666;">Avaliado por: {{item.review.user_name}} em {{item.review.timestamp.split('T')[0]}}</p>
        </li>
    % end
    </ul>
    % else:
    <p>Você ainda não fez nenhuma avaliação.</p>
    % end

    <p><a href="/movies">Voltar para a lista de filmes</a></p>
    </main>
    <footer>
        <hr>
        <p>&copy; 2025 Meu App de Filmes. Todos os direitos reservados.</p>
    </footer>
</body>
</html>