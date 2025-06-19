# app/services/financial_instrument_service.py
from app.repositories.financial_instrument_repository import FinancialInstrumentRepository
from app.models.models import InstrumentoFinanciero
from app import db
from sqlalchemy.exc import IntegrityError

class FinancialInstrumentService:
    def __init__(self):
        self.instrument_repo = FinancialInstrumentRepository()

    def create_instrument(self, data):
        nombre = data.get('nombre')
        tipo = data.get('tipo')
        simbolo = data.get('simbolo')

        if not nombre or not tipo or not simbolo:
            raise ValueError('Nombre, tipo, and simbolo are required.')

        if self.instrument_repo.get_by_symbol(simbolo):
            raise ValueError(f'Instrument with symbol {simbolo} already exists.')

        existing_by_name = InstrumentoFinanciero.query.filter_by(nombre=nombre).first()
        if existing_by_name:
            raise ValueError(f'Instrument with name {nombre} already exists.')

        instrument = InstrumentoFinanciero(nombre=nombre, tipo=tipo, simbolo=simbolo)
        try:
            return self.instrument_repo.add(instrument)
        except IntegrityError as e:
            db.session.rollback()
            # This is a bit generic, but IntegrityError could be due to unique constraints
            # which we've already checked. However, good to have a catch-all.
            raise ValueError(f'Could not create instrument due to a database integrity issue. Error: {e}')

    def get_instrument_by_id(self, instrument_id):
        instrument = self.instrument_repo.get_by_id(instrument_id)
        if not instrument:
            raise ValueError('Instrument not found by ID.') # Added for clarity in controller
        return instrument

    def get_instrument_by_symbol(self, simbolo):
        instrument = self.instrument_repo.get_by_symbol(simbolo)
        if not instrument:
            raise ValueError('Instrument not found by symbol.') # Added for clarity in controller
        return instrument

    def get_all_instruments(self):
        return self.instrument_repo.get_all()
