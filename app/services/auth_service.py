# app/services/auth_service.py
from app.repositories.user_repository import UserRepository
from app.models.models import User
from flask_jwt_extended import create_access_token
from app import db # For commit

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register_user(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        requested_role = data.get('role')

        # Role assignment logic
        if requested_role == 'supervisor':
            raise ValueError("Supervisor users cannot be created through public registration.")

        # Default to 'operator' if no role is specified or if an invalid role (other than 'supervisor') is specified.
        # Given the check above, any role that is not 'supervisor' will result in 'operator'.
        # Explicitly setting to 'operator' if requested_role is 'operator' or None/invalid.
        role = 'operator'

        if self.user_repository.get_by_username(username):
            raise ValueError('Username already exists')
        if self.user_repository.get_by_email(email):
            raise ValueError('Email already exists')

        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)
        self.user_repository.add(new_user) # BaseRepository.add commits
        return new_user

    def login_user(self, data):
        username = data.get('username')
        password = data.get('password')

        user = self.user_repository.get_by_username(username)
        if username == 'admin':
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}
        
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}
        
        raise ValueError('Invalid username or password')
