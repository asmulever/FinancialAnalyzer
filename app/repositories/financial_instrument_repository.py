# app/repositories/financial_instrument_repository.py
from app.models.models import InstrumentoFinanciero
from .base_repository import BaseRepository

class FinancialInstrumentRepository(BaseRepository):
    def __init__(self):
        super().__init__(InstrumentoFinanciero)

    def get_by_symbol(self, simbolo):
        return InstrumentoFinanciero.query.filter_by(simbolo=simbolo).first()
