from bottle import request
from models.user import UserModel, User
import bcrypt 

class UserService:
    def __init__(self):
        self.user_model = UserModel()


    def get_all(self):
        users = self.user_model.get_all()
        return users


    def save(self):
        last_id = max([u.id for u in self.user_model.get_all()], default=0)
        new_id = last_id + 1
        name = request.forms.get('name')
        email = request.forms.get('email')
        raw_senha = request.forms.get('senha')
        birthdate = request.forms.get('birthdate')

        hashed_senha = bcrypt.hashpw(raw_senha.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
        user = User(id=new_id, name=name, email=email, birthdate=birthdate, senha=hashed_senha)
        self.user_model.add_user(user)


    def get_by_id(self, user_id):
        return self.user_model.get_by_id(user_id)


    def edit_user(self, user):
        name = request.forms.get('name')
        email = request.forms.get('email')
        raw_senha = request.forms.get('senha')
        birthdate = request.forms.get('birthdate')
        
        user.name = name
        user.email = email
        user.birthdate = birthdate

        if raw_senha:
            hashed_senha = bcrypt.hashpw(raw_senha.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
            user.senha = hashed_senha

        self.user_model.update_user(user)


    def delete_user(self, user_id):
        self.user_model.delete_user(user_id)

    def check_credentials(self, email, raw_password):
        user = self.user_model.get_by_email(email)

        if user:
    
            if bcrypt.checkpw(raw_password.encode('utf-8'), user.senha.encode('utf-8')):
                return user 
        return None 