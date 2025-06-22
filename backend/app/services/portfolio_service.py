# app/services/portfolio_service.py
from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.financial_instrument_repository import FinancialInstrumentRepository
from app.repositories.market_data_repository import MarketDataRepository
from app.models.models import HistoricoMovimiento, Cartera, InstrumentoFinanciero
from app import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError

class PortfolioService:
    def __init__(self):
        self.portfolio_repo = PortfolioRepository()
        self.instrument_repo = FinancialInstrumentRepository()
        self.market_data_repo = MarketDataRepository()

    def create_portfolio(self, data):
        nombre = data.get('nombre')
        propietario = data.get('propietario')
        if not nombre:
            raise ValueError('Portfolio name is required.')
        existing_portfolio = Cartera.query.filter_by(nombre=nombre).first() # Check for uniqueness
        if existing_portfolio:
            raise ValueError(f'Portfolio with name "{nombre}" already exists.')
        cartera = Cartera(nombre=nombre, propietario=propietario)
        return self.portfolio_repo.add(cartera)

    def get_all_portfolios(self):
        return self.portfolio_repo.get_all()

    def get_portfolio_by_id(self, portfolio_id):
        portfolio = self.portfolio_repo.get_by_id(portfolio_id)
        if not portfolio:
            raise ValueError('Portfolio not found')
        return portfolio

    def add_instrument_to_portfolio(self, portfolio_id, movement_data):
        portfolio = self.get_portfolio_by_id(portfolio_id)
        instrumento_simbolo = movement_data.get('instrumento_simbolo')
        instrumento = self.instrument_repo.get_by_symbol(instrumento_simbolo)
        if not instrumento:
            raise ValueError(f'Instrument with symbol {instrumento_simbolo} not found.')

        cantidad = movement_data.get('cantidad')
        precio_unitario = movement_data.get('precio_unitario')
        tipo_operacion = movement_data.get('tipo_operacion', 'compra').lower()
        fecha_str = movement_data.get('fecha') # Expects YYYY-MM-DD HH:MM:SS or YYYY-MM-DD

        if not all([cantidad, precio_unitario, tipo_operacion]):
            raise ValueError('Missing cantidad, precio_unitario or tipo_operacion for the movement.')
        if tipo_operacion not in ['compra', 'venta']:
            raise ValueError('tipo_operacion must be "compra" or "venta".')

        fecha_operacion = datetime.utcnow()
        if fecha_str:
            try:
                if len(fecha_str) == 10: # YYYY-MM-DD
                    fecha_operacion = datetime.strptime(fecha_str, '%Y-%m-%d')
                else: # YYYY-MM-DD HH:MM:SS
                    fecha_operacion = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS.')

        # For 'venta', ensure sufficient quantity is owned (simplified check)
        if tipo_operacion == 'venta':
            current_holdings = self.get_portfolio_holdings(portfolio_id)
            instrument_holding = next((h for h in current_holdings if h['instrumento_id'] == instrumento.id), None)
            if not instrument_holding or instrument_holding['net_quantity'] < cantidad:
                raise ValueError(f'Insufficient quantity of {instrumento_simbolo} to sell.')

        movimiento = HistoricoMovimiento(
            cartera_id=portfolio.id,
            instrumento_id=instrumento.id,
            fecha=fecha_operacion,
            cantidad=float(cantidad),
            precio_unitario=float(precio_unitario),
            tipo_operacion=tipo_operacion
        )
        try:
            db.session.add(movimiento)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError('Error saving movement to database.')
        return movimiento

    def get_portfolio_holdings(self, portfolio_id):
        self.get_portfolio_by_id(portfolio_id) # Validate portfolio exists
        movements = self.portfolio_repo.get_movements_for_portfolio(portfolio_id)
        holdings = {}
        for mov in movements:
            instrument_info = holdings.setdefault(mov.instrumento_id, {
                'instrumento_id': mov.instrumento_id,
                'simbolo': mov.instrumento.simbolo,
                'nombre': mov.instrumento.nombre,
                'net_quantity': 0,
                'total_cost': 0.0,
                'current_value': 0.0,
                'average_buy_price': 0.0
            })
            if mov.tipo_operacion == 'compra':
                instrument_info['net_quantity'] += mov.cantidad
                instrument_info['total_cost'] += mov.cantidad * mov.precio_unitario
            elif mov.tipo_operacion == 'venta':
                instrument_info['net_quantity'] -= mov.cantidad
                # Cost basis reduction can be complex; simplified here
                # This assumes sales reduce cost at the average buy price up to that point
                if instrument_info['net_quantity'] + mov.cantidad > 0: # if there were shares before this sale
                    avg_price_before_sale = instrument_info['total_cost'] / (instrument_info['net_quantity'] + mov.cantidad)
                    instrument_info['total_cost'] -= mov.cantidad * avg_price_before_sale
                else: # Selling shares that were not tracked or over-selling (data issue)
                    pass # Or handle error

        # Calculate current value and average buy price
        for instrument_id, info in holdings.items():
            if info['net_quantity'] > 0:
                info['average_buy_price'] = round(info['total_cost'] / info['net_quantity'], 2) if info['net_quantity'] > 0 else 0
                latest_price_obj = self.market_data_repo.get_latest_price(instrument_id)
                if latest_price_obj:
                    info['current_value'] = round(info['net_quantity'] * latest_price_obj.precio_cierre, 2)
            else: # If net quantity is zero or negative, reset cost and value
                info['total_cost'] = 0.0
                info['current_value'] = 0.0
                info['average_buy_price'] = 0.0

        return [info for info in holdings.values() if info['net_quantity'] > 0] # Only return current holdings

    def get_portfolio_summary(self, portfolio_id):
        portfolio = self.get_portfolio_by_id(portfolio_id)
        holdings = self.get_portfolio_holdings(portfolio_id)
        total_portfolio_value = sum(h['current_value'] for h in holdings)
        total_portfolio_cost = sum(h['total_cost'] for h in holdings)
        overall_pnl = total_portfolio_value - total_portfolio_cost
        overall_pnl_percent = (overall_pnl / total_portfolio_cost * 100) if total_portfolio_cost != 0 else 0

        return {
            'portfolio_id': portfolio.id,
            'portfolio_nombre': portfolio.nombre,
            'total_current_value': round(total_portfolio_value, 2),
            'total_cost_basis': round(total_portfolio_cost, 2),
            'overall_pnl': round(overall_pnl, 2),
            'overall_pnl_percent': round(overall_pnl_percent, 2),
            'holdings': holdings
        }
