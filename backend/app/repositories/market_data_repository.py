# app/repositories/market_data_repository.py
from app.models.models import MonitorAccion # Or PrecioHistoricoInstrumento
from .base_repository import BaseRepository
from app import db
from datetime import datetime

class MarketDataRepository(BaseRepository):
    def __init__(self):
        super().__init__(MonitorAccion)

    def get_prices_for_instrument(self, instrumento_id, start_date=None, end_date=None):
        query = MonitorAccion.query.filter_by(instrumento_id=instrumento_id)
        if start_date:
            query = query.filter(MonitorAccion.fecha >= start_date)
        if end_date:
            query = query.filter(MonitorAccion.fecha <= end_date)
        return query.order_by(MonitorAccion.fecha.asc()).all()

    def get_latest_price(self, instrumento_id):
        return MonitorAccion.query.filter_by(instrumento_id=instrumento_id).order_by(MonitorAccion.fecha.desc()).first()
