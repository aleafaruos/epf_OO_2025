from bottle import Bottle
from controllers.user_controller import user_routes
from controllers.movie_controller import movie_routes

def init_controllers(app: Bottle):
    app.merge(user_routes)
    app.merge(movie_routes)
   



