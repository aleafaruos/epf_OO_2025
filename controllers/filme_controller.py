# Arquivo: controllers/filme_controller.py

from bottle import route, template, Bottle # Importe Bottle para criar um objeto de rotas

filme_routes = Bottle() # Criamos uma instância Bottle para agrupar as rotas de filmes

@filme_routes.route('/filmes', method='GET')
def mostrar_pagina_filmes():
    """Renderiza a página principal de filmes."""
    # 'template' é importado do Bottle, então não precisa de self.render aqui
    return template('filmes.tpl', title='Lista de Filmes')

# A rota de arquivos estáticos geralmente fica no BaseController e é global,
# então você não precisa duplicá-la aqui. O BaseController (que já tem essa rota)
# deve ser incluído via init_controllers também.