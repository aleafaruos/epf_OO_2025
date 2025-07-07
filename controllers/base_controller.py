from bottle import static_file, redirect as bottle_redirect, template as render_template

class BaseController:
    def __init__(self, app):
        self.app = app
        self._setup_base_routes()

    def _setup_base_routes(self):
        self.app.route('/', method='GET', callback=self.home_redirect)
        self.app.route('/static/<filename:path>', callback=self.serve_static)

    def home_redirect(self):
        """Redireciona a rota raiz para a página de filmes, que é a nossa página inicial."""
        return self.redirect('/movies')

    def serve_static(self, filename):
        """Serve arquivos estáticos da pasta static/"""
        return static_file(filename, root='./static')

    def render(self, template, **context):
        """Método auxiliar para renderizar templates."""
        return render_template(template, **context)

    def redirect(self, path):
        """Método auxiliar para redirecionamento."""
        return bottle_redirect(path)