from bottle import Bottle
from controllers.user_controller import user_routes
from controllers.movie_controller import movie_routes
from controllers.avaliacao_controller import avaliacao_routes

def init_controllers(app: Bottle):
    app.merge(user_routes)
    app.merge(movie_routes)
    app.merge(avaliacao_routes)
   



