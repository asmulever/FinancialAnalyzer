# app/repositories/user_repository.py
from app.models.models import User
from .base_repository import BaseRepository
from app import db

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()
