<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ locals().get('title', 'CineReviews') }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-custom">
    <div class="container-fluid">
        <a class="navbar-brand brand-title" href="/movies">CINEREVIEWS</a>
        <div class="collapse navbar-collapse">
            <form class="d-flex mx-auto search-container" action="/movies" method="get">
                <input class="form-control me-2 search-bar" type="search" name="termo_busca" placeholder="Buscar filmes..." aria-label="Search" value="{{ locals().get('termo_busca', '') }}">
                <button class="btn btn-outline-light" type="submit">Buscar</button>
            </form>

            <ul class="navbar-nav ms-auto">
                % if defined('logged_in_user') and logged_in_user:
                    <li class="nav-item">
                        <a class="nav-link text-white" href="/profile" title="Meu Perfil">
                            <i class="fas fa-user-circle me-1"></i>
                            {{ logged_in_user.name }}
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-white" href="/logout" title="Sair">Sair</a>
                    </li>
                % else:
                    <li class="nav-item">
                        <button type="button" class="btn btn-outline-light me-2" data-bs-toggle="modal" data-bs-target="#loginModal">
                            Login
                        </button>
                    </li>
                    <li class="nav-item">
                        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#registerModal">
                            Criar Conta
                        </button>
                    </li>
                % end
            </ul>
        </div>
    </div>
</nav>

<main>
    {{!base}}
</main>

% if not (defined('logged_in_user') and logged_in_user):
    <div class="modal fade" id="loginModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog"><div class="modal-content">
          <div class="modal-header"><h5 class="modal-title">Login</h5><button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button></div>
          <div class="modal-body">
            <form id="loginForm">
              <div class="mb-3"><input type="email" class="form-control" name="email" placeholder="Email" required></div>
              <div class="mb-3"><input type="password" class="form-control" name="senha" placeholder="Senha" required></div>
              <div id="login-error-message" class="alert alert-danger" style="display: none;"></div>
              <button type="submit" class="btn btn-primary w-100">Entrar</button>
            </form>
          </div>
    </div></div></div>
    <div class="modal fade" id="registerModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog"><div class="modal-content">
          <div class="modal-header"><h5 class="modal-title">Criar Conta</h5><button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button></div>
          <div class="modal-body">
            <form id="registerForm">
              <div class="mb-3"><input type="text" class="form-control" name="name" placeholder="Nome" required></div>
              <div class="mb-3"><input type="email" class="form-control" name="email" placeholder="Email" required></div>
              <div class="mb-3"><input type="password" class="form-control" name="senha" placeholder="Senha" required></div>
              <div class="mb-3"><input type="date" class="form-control" name="birthdate" placeholder="Data de Nascimento" required></div>
              <div id="register-error-message" class="alert alert-danger" style="display: none;"></div>
              <button type="submit" class="btn btn-primary w-100">Cadastrar</button>
            </form>
          </div>
    </div></div></div>
% end

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script src="/static/auth.js"></script>

% if defined('page_js'):
    <script src="{{ page_js }}"></script>
% end

</body>
</html>