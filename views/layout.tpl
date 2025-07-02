<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>{{title or 'CineReviews'}}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Anton&display=swap" rel="stylesheet">
    <link href="/static/css/style.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom">
    <div class="container-fluid">
        <a class="navbar-brand brand-title" href="/movies">CineReviews</a>
        <div class="ms-auto">
            <ul class="navbar-nav">
                %if defined('logged_in_user') and logged_in_user:
                    <li class="nav-item">
                        <span class="navbar-text me-3">Olá, {{logged_in_user.name}}!</span>
                    </li>
                    <li class="nav-item">
                        <a class="btn btn-outline-light" href="/logout">Logout</a>
                    </li>
                %else:
                    <li class="nav-item">
                        <button type="button" class="btn btn-outline-light" data-bs-toggle="modal" data-bs-target="#loginModal">
                            Login
                        </button>
                    </li>
                    <li class="nav-item">
                        <button type="button" class="btn btn-primary ms-2" data-bs-toggle="modal" data-bs-target="#registerModal">
                            Criar Conta
                        </button>
                    </li>
                %end
            </ul>
        </div>
    </div>
</nav>

    <main>
        {{!base}} 
    </main>

    <div class="modal fade" id="loginModal" tabindex="-1" aria-labelledby="loginModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="loginModalLabel">Login de Usuário</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form class="auth-form" action="/login" method="post">
                      <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" class="form-control" id="email" name="email" required>
                      </div>
                      <div class="form-group">
                        <label for="senha">Senha</label>
                        <input type="password" class="form-control" id="senha" name="senha" required>
                      </div>
                      <button type="submit" class="btn btn-primary btn-block mt-4">Entrar</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" id="registerModal" tabindex="-1" aria-labelledby="registerModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="registerModalLabel">Crie sua Conta</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form class="auth-form" action="/users/add" method="post">
                      <div class="form-group">
                        <label for="name">Nome Completo</label>
                        <input type="text" class="form-control" id="name" name="name" required>
                      </div>
                      <div class="form-group">
                        <label for="email_reg">Email</label>
                        <input type="email" class="form-control" id="email_reg" name="email" required>
                      </div>
                      <div class="form-group">
                        <label for="birthdate">Data de Nascimento</label>
                        <input type="date" class="form-control" id="birthdate" name="birthdate" required>
                      </div>
                      <div class="form-group">
                        <label for="senha_reg">Senha</label>
                        <input type="password" class="form-control" id="senha_reg" name="senha" required>
                      </div>
                      <button type="submit" class="btn btn-primary btn-block mt-4">Criar Conta</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

    <script>
  document.querySelector('#registerModal form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Impede o envio tradicional do formulário

    const form = event.target;
    const formData = new FormData(form);

    const response = await fetch('/users/add', {
      method: 'POST',
      body: formData
    });

    if (response.redirected) {
      window.location.href = response.url; // Redireciona corretamente
    }
  });
</script>
</body>
</html>
