# app/services/analysis_service.py
from app.repositories.financial_instrument_repository import FinancialInstrumentRepository
from app.repositories.market_data_repository import MarketDataRepository
from datetime import datetime, timedelta

class AnalysisService:
    def __init__(self):
        self.instrument_repo = FinancialInstrumentRepository()
        self.market_data_repo = MarketDataRepository()

    def get_instrument_analysis(self, instrument_id_or_symbol):
        instrument = None
        if isinstance(instrument_id_or_symbol, int):
            instrument = self.instrument_repo.get_by_id(instrument_id_or_symbol)
        elif isinstance(instrument_id_or_symbol, str):
            instrument = self.instrument_repo.get_by_symbol(instrument_id_or_symbol)

        if not instrument:
            raise ValueError('Instrument not found')

        # Calculate some basic analysis, e.g., recent return
        # For simplicity, let's try to get last 2 prices to calculate return
        # In a real scenario, you'd want more robust date handling and period selection

        # Get last 30 days of prices, for example
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)

        prices_data = self.market_data_repo.get_prices_for_instrument(
            instrument_id=instrument.id,
            start_date=start_date,
            end_date=end_date
        )

        analysis_result = {
            'instrument_id': instrument.id,
            'instrument_symbol': instrument.simbolo,
            'instrument_nombre': instrument.nombre,
            'period_return': None,
            'latest_price': None,
            'price_data_points': len(prices_data),
            'message': ''
        }

        if prices_data and len(prices_data) > 1:
            # Sort by date just in case they are not already
            prices_data.sort(key=lambda x: x.fecha)
            oldest_price_point = prices_data[0]
            latest_price_point = prices_data[-1]

            analysis_result['latest_price'] = latest_price_point.precio_cierre

            if oldest_price_point.precio_cierre != 0:
                period_return = ((latest_price_point.precio_cierre - oldest_price_point.precio_cierre) / oldest_price_point.precio_cierre) * 100
                analysis_result['period_return'] = round(period_return, 2) # Percentage
            else:
                analysis_result['message'] = 'Oldest price is zero, cannot calculate return.'
        elif prices_data and len(prices_data) == 1:
            analysis_result['latest_price'] = prices_data[0].precio_cierre
            analysis_result['message'] = 'Only one data point available for the period.'
        else:
            latest_price_obj = self.market_data_repo.get_latest_price(instrument.id)
            if latest_price_obj:
                analysis_result['latest_price'] = latest_price_obj.precio_cierre
            analysis_result['message'] = 'Not enough price data available for the selected period to calculate return.'

        return analysis_result
