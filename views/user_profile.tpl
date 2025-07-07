% rebase('layout.tpl', title='Perfil de ' + user.name, logged_in_user=user)

<div class="container profile-page-container">
    <header class="profile-page-header">
        <h1 class="profile-page-username">{{ user.name }}</h1>
    </header>

    <div class="row gx-5">
        <div class="col-md-8">
            <section class="reviews-section">
                <h2 class="section-title">ATIVIDADE RECENTE</h2>
                % if not user_reviews:
                    <p class="text-muted">Nenhuma avaliação para mostrar.</p>
                % else:
                    <ul class="profile-review-list">
                        % for review in user_reviews:
                        <li class="profile-review-item">
                            <div class="profile-review-poster">
                                <a href="/movies/{{ review['movie_details']['id'] }}">
                                    <img src="https://image.tmdb.org/t/p/w500{{ review['movie_details']['poster_path'] }}" alt="Poster de {{ review['movie_details']['title'] }}">
                                </a>
                            </div>
                            <div class="profile-review-details">
                                <h3 class="profile-review-movie-title">
                                    <a href="/movies/{{ review['movie_details']['id'] }}">{{ review['movie_details']['title'] }}</a>
                                    <span class="profile-review-movie-year">{{ review['movie_details']['release_date'][:4] if review['movie_details']['release_date'] else '' }}</span>
                                </h3>
                                <div class="profile-review-rating">
                                    <span class="star-rating-display">
                                        % nota = int(review.get('nota', 0))
                                        {{ '★' * nota }}{{ '☆' * (5 - nota) }}
                                    </span>
                                </div>
                                % if review.get('comentario'):
                                    <p class="profile-review-comment">“{{ review.get('comentario') }}”</p>
                                % end
                            </div>
                        </li>
                        % end
                    </ul>
                % end
            </section>
        </div>

        <div class="col-md-4">
            <aside class="favorites-sidebar">
                <h2 class="section-title">FAVORITOS</h2>
                % if not user_favorites:
                    <p class="text-muted">Nenhum filme favorito ainda.</p>
                % else:
                    <div class="favorite-posters-grid">
                        % for movie in user_favorites:
                            <div class="favorite-poster-container">
                                <a href="/movies/{{ movie['id'] }}" title="{{ movie['title'] }}">
                                    <img src="https://image.tmdb.org/t/p/w500{{ movie['poster_path'] }}" alt="{{ movie['title'] }}" class="favorite-poster-img">
                                </a>
                            </div>
                        % end
                    </div>
                % end
            </aside>
        </div>
    </div>
</div>