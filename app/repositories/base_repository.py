# app/repositories/base_repository.py
from app import db

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return db.session.query(self.model).all()

    def get_by_id(self, id):
        return db.session.query(self.model).get(id)

    def add(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity

    def update(self, entity):
        db.session.commit()
        return entity

    def delete(self, entity):
        db.session.delete(entity)
        db.session.commit()
