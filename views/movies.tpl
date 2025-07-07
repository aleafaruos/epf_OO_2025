%rebase('layout.tpl', title='Bem-vindo ao CineReviews')

%rebase('layout.tpl', title='Bem-vindo ao CineReviews')

<header class="hero-section">
    <div class="movie-montage-background">
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/1OsQJEoSXBjduuCvDOlRhoEUaHu.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/nCbkOyOMTEwlEV0LtCOvCnwEONA.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/uP46DujkD3nwcisOjz9a0Xw0Knj.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/tptjnB2LDbuUWya9Cx5sQtv5hqb.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/yRRuLt7sMBEQkHsd1S3KaaofZn7.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/8qBccgSj0Ru9Odm1Mjv82cxDr7l.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/R1ieKOdGHYL7BRpl0iRgNV1uXw.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/lRRMQhlOLM9xgvjKKFndOmptqKR.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/bik2BZjmVjeE6LOZqtuTjb4jJPQ.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/bW21kbvqAt2kMGlaU8qY86C8kQE.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/omoMXT3Z7XrQwRZ2OGJGNWbdeEl.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/fUwfsPWEEdnSt29jIwJ5eVtySX6.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/f5HBqwNATnuUJjD997WII7IF3WX.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/bAJWDxfTSH2zbqUI5YgvWuKhvrj.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/xLxgVxFWvb9hhUyCDDXxRPPnFck.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/ohXr0v9U0TfFu9IXbSDm5zoGV3R.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/9yaVKBwvbvq3qL8zzSmuoxZuoFK.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/4rxEeTzN1oZPJo1GBoPOnA3NeJv.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/d74WpIsH8379TIL4wUxDneRCYv2.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/cKNxg77ll8caX3LulREep4C24Vx.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/pA70WUs7KHiHltfiBN4XEELOXcS.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/azm7busQSOm5I0QVR0nff8mC2Jk.jpg" alt="Pôster"></div>
        <div class="montage-image"><img src="https://image.tmdb.org/t/p/original/8OGQCOp6BxwvekhZBQCzVd77Y6l.jpg" alt="Pôster"></div>
    </div>

    <div class="hero-text">
        <h1>Descubra. Assista. Relembre.</h1>
        <p>Sua jornada pelo cinema começa aqui. Organize os filmes que você assistiu e descubra novos favoritos.</p>
    </div>
</header>

<section class="content-section">
    <div class="container movies-container">
        <h2 class="movies-page-title">Filmes em Destaque</h2>
        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
            % for movie in movies:
    <div class="col">
        <div class="card h-100">
            
            <a href="/movies/{{movie.id}}">
                <img src="{{movie.poster}}" class="card-img-top" alt="Pôster de {{movie.name}}">
            </a>

            <div class="card-body d-flex flex-column">
                <h5 class="card-title">
                    <a href="/movies/{{movie.id}}" style="color: #fff; text-decoration: none;">{{movie.name}}</a>
                </h5>

                <div class="card-text text-light mb-3"> 
                    % if hasattr(movie, 'ano') and movie.ano:
                        <span>Ano: {{ movie.ano[:4] }}</span>
                    % else:
                        <span>Ano: N/A</span>
                    % end
                    <br>
                    <span>
                        <i class="fas fa-star" style="color: #ffc107;"></i>
                        {{ "%.1f" % movie.avaliacao_media }} ({{ movie.numero_votos }} votos)
                    </span>
                </div>

                <a href="/movies/{{movie.id}}" class="btn btn-primary mt-auto">Ver Detalhes</a>
            </div>
        </div>
    </div>
% end
        </div>
    </div>
</section>
