%# CORREÇÃO: Passa a variável page_js para o layout.tpl carregar o script
% rebase('layout.tpl', title=movie.get('title', 'Detalhes'), page_js='/static/js/movie_details.js', logged_in_user=logged_in_user)

% if error_message:
    <div class="alert alert-danger">{{ error_message }}</div>
% else:
    <div class="movie-details-backdrop" style="background-image: url('https://image.tmdb.org/t/p/original{{ movie.get("backdrop_path") }}');"></div>

    <div class="container movie-details-container" style="position: relative; z-index: 2;">
        <div class="row">
            <div class="col-md-4 text-center">
                <img src="https://image.tmdb.org/t/p/w500{{ movie.get('poster_path') }}" alt="{{ movie.get('title') }}" class="img-fluid movie-poster-details">
            </div>
            <div class="col-md-8 movie-info">

                <div style="display: flex; align-items: center; justify-content: space-between;">
    <h1 class="movie-title mb-0">{{ movie.get('title') }}</h1>
    
    % if logged_in_user:
        <form action="/filme/favoritar" method="POST" style="display: inline-block; line-height: 1;">
            
            <input type="hidden" name="id_filme" value="{{ movie.get('id') }}">
            
            % is_favorite = movie.get('id') in logged_in_user.favorites
            
            <button type="submit"
                    title="{{'Remover dos Favoritos' if is_favorite else 'Adicionar aos Favoritos'}}"
                    style="background: none; border: none; padding: 0; line-height: 1;">
                    
                <i class="fas fa-heart favorite-heart {{'favorited' if is_favorite else ''}}"></i>
            </button>
        </form>
    % end
</div>
                <p class="movie-tagline">{{ movie.get('tagline') }}</p>
                <div class="movie-stats">
                    <span><i class="fas fa-calendar-alt"></i> {{ movie.get('release_date', 'N/A')[:4] }}</span>
                    <span><i class="fas fa-star"></i> {{ "%.1f" % movie.get('vote_average', 0) }}/10</span>
                    <span><i class="fas fa-clock"></i> {{ movie.get('runtime', 0) }} min</span>
                </div>
                <h4>Sinopse</h4>
                <p>{{ movie.get('overview', 'Sinopse não disponível.') }}</p>
                
                % if logged_in_user:
                <div class="rating-section mt-5">
                    <h4>Deixe sua avaliação</h4>
                    <form action="/avaliacoes/add" method="post">
                        <input type="hidden" name="id_filme" value="{{ movie.get('id') }}">
                        <input type="hidden" name="id_usuario" value="{{ logged_in_user.id }}">
                        <div class="mb-3">
                            <label class="form-label">Nota:</label>
                            <div class="star-rating" data-rating="0">
                                <span class="star" data-value="1">★</span><span class="star" data-value="2">★</span><span class="star" data-value="3">★</span><span class="star" data-value="4">★</span><span class="star" data-value="5">★</span>
                            </div>
                            <input type="hidden" name="nota" id="rating-value" required>
                        </div>
                        <div class="mb-3">
                            <textarea class="form-control rating-input" name="comentario" rows="3" placeholder="Escreva um comentário (opcional)..."></textarea>
                        </div>
                        <button type="submit" class="btn btn-success">Enviar Avaliação</button>
                    </form>
                </div>
                % else:
                <div class="alert alert-info mt-5">
                    <a href="#" data-bs-toggle="modal" data-bs-target="#loginModal">Faça login</a> para deixar uma avaliação.
                </div>
                % end
            </div>
        </div>

        <div class="row mt-5">
            <div class="col-12 existing-reviews-section">
                <h4>Comentários da Comunidade</h4>
                % if not reviews:
                    <p>Ainda não há comentários para este filme.</p>
                % else:
                    % for review in reviews:
                    <div class="review-card"><div class="review-card-header">
                        <strong>{{ review.get('nome_usuario', 'Anônimo') }}</strong>
                        <span class="review-card-rating">
                            % nota = int(review.get('nota', 0))
                            {{ '★' * nota }}
                        </span>
                    </div><div class="review-card-body">
                        <p>{{ review.get('comentario', 'Nenhum comentário escrito.') }}</p>
                    </div></div>
                    % end
                % end
            </div>
        </div>
    </div>
    <script src="/static/js/star-rating.js"></script>
% end