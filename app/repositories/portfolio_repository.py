# app/repositories/portfolio_repository.py
from app.models.models import Cartera, HistoricoMovimiento
from .base_repository import BaseRepository
from app import db

class PortfolioRepository(BaseRepository):
    def __init__(self):
        super().__init__(Cartera)

    def add_movement(self, movimiento_data):
        movimiento = HistoricoMovimiento(**movimiento_data)
        db.session.add(movimiento)
        db.session.commit()
        return movimiento

    def get_movements_for_portfolio(self, cartera_id):
        return HistoricoMovimiento.query.filter_by(cartera_id=cartera_id).all()
