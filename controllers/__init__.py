from bottle import Bottle
from controllers.user_controller import user_routes
from controllers.filme_controller import filme_routes 
from controllers.base_controller import BaseController 

def init_controllers(app: Bottle):
    app.merge(user_routes)
    app.merge(filme_routes)



