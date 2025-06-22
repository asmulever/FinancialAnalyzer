# app/services/suggestion_service.py
from app.services.portfolio_service import PortfolioService
from app.services.analysis_service import AnalysisService
from datetime import datetime # Added for utcnow

class SuggestionService:
    def __init__(self):
        self.portfolio_service = PortfolioService()
        self.analysis_service = AnalysisService()

    def generate_suggestions(self, portfolio_id):
        # Validate portfolio
        try:
            portfolio_summary = self.portfolio_service.get_portfolio_summary(portfolio_id)
        except ValueError as e:
            raise ValueError(f"Could not retrieve portfolio for suggestions: {str(e)}")

        suggestions = []

        # Placeholder for suggestion logic
        # This is where more complex rules or ML models could be integrated.

        # Example: Suggest rebalancing if a holding is too concentrated
        MAX_HOLDING_PERCENTAGE = 40.0 # Example threshold: 40% of portfolio value
        total_portfolio_value = portfolio_summary['total_current_value']

        if total_portfolio_value > 0:
            for holding in portfolio_summary['holdings']:
                holding_percentage = (holding['current_value'] / total_portfolio_value) * 100
                if holding_percentage > MAX_HOLDING_PERCENTAGE:
                    suggestions.append({
                        'type': 'rebalance_concentration',
                        'instrument_simbolo': holding['simbolo'],
                        'instrument_nombre': holding['nombre'],
                        'current_percentage': round(holding_percentage, 2),
                        'message': f"Consider reducing exposure to {holding['simbolo']}, as it represents {round(holding_percentage, 2)}% of your portfolio (threshold: {MAX_HOLDING_PERCENTAGE}%)."
                    })

        # Example: Suggest diversifying if portfolio has too few holdings
        MIN_HOLDINGS_COUNT = 3 # Example threshold
        if len(portfolio_summary['holdings']) < MIN_HOLDINGS_COUNT and len(portfolio_summary['holdings']) > 0:
            suggestions.append({
                'type': 'diversify_portfolio',
                'message': f"Your portfolio has only {len(portfolio_summary['holdings'])} holding(s). Consider diversifying by adding at least {MIN_HOLDINGS_COUNT - len(portfolio_summary['holdings'])} more instruments."
            })
        elif not portfolio_summary['holdings']:
            suggestions.append({
                'type': 'empty_portfolio',
                'message': 'Your portfolio is currently empty. Consider adding some instruments to start investing.'
            })

        if not suggestions and portfolio_summary['holdings']:
            suggestions.append({'type': 'general_ok', 'message': 'Portfolio looks reasonably balanced based on current basic checks.'})

        return {
            'portfolio_id': portfolio_id,
            'portfolio_nombre': portfolio_summary['portfolio_nombre'],
            'generated_at': datetime.utcnow().isoformat(),
            'suggestions': suggestions
        }
