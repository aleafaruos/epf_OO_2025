from bottle import Bottle
from controllers.user_controller import user_routes
from controllers.base_controller import BaseController 

def init_controllers(app: Bottle):
    app.merge(user_routes)
   



