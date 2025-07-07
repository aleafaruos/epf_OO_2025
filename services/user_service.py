from bottle import request
from models.user import UserModel, User
import bcrypt

class UserService:
    def __init__(self):
        self.user_model = UserModel()

    def get_all(self):
        return self.user_model.get_all()

    def get_by_id(self, user_id):
        return self.user_model.get_by_id(user_id)

    def save(self):
        name = request.forms.get('name')
        email = request.forms.get('email')
        raw_senha = request.forms.get('senha')
        birthdate = request.forms.get('birthdate')

        if self.user_model.get_by_email(email):
            raise ValueError(f"O e-mail '{email}' já está em uso. Por favor, escolha outro.")

        last_id = max([u.id for u in self.get_all()], default=0) if self.get_all() else 0
        new_id = last_id + 1
        
        hashed_senha = bcrypt.hashpw(raw_senha.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
        new_user = User(id=new_id, name=name, email=email, birthdate=birthdate, senha=hashed_senha)
        
        self.user_model.add_user(new_user)
        return new_user

    def check_credentials(self, email, raw_password):
        user = self.user_model.get_by_email(email)
        if user and bcrypt.checkpw(raw_password.encode('utf-8'), user.senha.encode('utf-8')):
            return user
        return None
    
    def toggle_favorite(self, user_id, movie_id):
        """
        Adiciona um filme aos favoritos se não estiver na lista,
        ou remove se já estiver. Retorna o novo estado (True se favorito).
        """
        user = self.get_by_id(user_id)
        if not user:
            return None 

        movie_id_int = int(movie_id)

        if movie_id_int in user.favorites:
            user.favorites.remove(movie_id_int)
            is_now_favorite = False
        else:
            user.favorites.append(movie_id_int)
            is_now_favorite = True
            
        self.user_model.update_user(user)
        return is_now_favorite