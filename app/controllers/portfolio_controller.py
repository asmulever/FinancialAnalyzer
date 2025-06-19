# app/controllers/portfolio_controller.py
from flask import Blueprint, request, jsonify
from app.services.portfolio_service import PortfolioService
from app.services.suggestion_service import SuggestionService
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity

portfolio_bp = Blueprint('portfolios', __name__, url_prefix='/portfolios')
portfolio_service = PortfolioService()
suggestion_service = SuggestionService()

@portfolio_bp.route('/', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Portfolios'],
    'summary': 'Create a new portfolio.',
    'security': [{'BearerAuth': []}],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'nombre': {'type': 'string', 'example': 'My Tech Portfolio'},
                        'propietario': {'type': 'string', 'example': 'user_id_or_name'}
                    },
                    'required': ['nombre']
                }
            }
        }
    },
    'responses': {
        '201': {'description': 'Portfolio created successfully.'},
        '400': {'description': 'Invalid input or portfolio name already exists.'},
        '401': {'description': 'Unauthorized.'}
    }
})
def create_portfolio():
    data = request.get_json()
    # In a real app, 'propietario' might be linked to get_jwt_identity()
    # For now, allowing it to be set from request or could default to current user
    # data['propietario'] = data.get('propietario', get_jwt_identity()) # Example if linking to user
    try:
        portfolio = portfolio_service.create_portfolio(data)
        return jsonify({'message': 'Portfolio created', 'portfolio': {'id': portfolio.id, 'nombre': portfolio.nombre, 'propietario': portfolio.propietario}}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@portfolio_bp.route('/', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Portfolios'],
    'summary': 'Get all portfolios (admin or user-specific in future).',
    'description': 'Currently retrieves all portfolios. Future enhancements could filter by owner based on JWT identity.',
    'security': [{'BearerAuth': []}],
    'responses': {
        '200': {'description': 'List of portfolios.'},
        '401': {'description': 'Unauthorized.'}
    }
})
def get_all_portfolios():
    # current_user_id = get_jwt_identity() # For future user-specific filtering
    portfolios = portfolio_service.get_all_portfolios()
    return jsonify([{'id': p.id, 'nombre': p.nombre, 'propietario': p.propietario} for p in portfolios]), 200

@portfolio_bp.route('/<int:portfolio_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Portfolios'],
    'summary': 'Get a specific portfolio by ID.',
    'description': 'Retrieves details for a specific portfolio. Future enhancements could check ownership against JWT identity.',
    'security': [{'BearerAuth': []}],
    'parameters': [{'name': 'portfolio_id', 'in': 'path', 'required': True, 'schema': {'type': 'integer'}}],
    'responses': {
        '200': {'description': 'Portfolio details.'},
        '401': {'description': 'Unauthorized.'},
        '404': {'description': 'Portfolio not found.'}
    }
})
def get_portfolio(portfolio_id):
    try:
        portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)
        # current_user_id = get_jwt_identity()
        # if str(portfolio.propietario) != str(current_user_id): # Assuming propietario is user ID
        #     return jsonify({'message': 'Forbidden: You do not own this portfolio'}), 403
        return jsonify({'id': portfolio.id, 'nombre': portfolio.nombre, 'propietario': portfolio.propietario}), 200
    except ValueError as e: # Catches 'Portfolio not found' from service
        return jsonify({'message': str(e)}), 404

@portfolio_bp.route('/<int:portfolio_id>/summary', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Portfolios'],
    'summary': 'Get a summary of a portfolio including holdings and performance.',
    'security': [{'BearerAuth': []}],
    'parameters': [{'name': 'portfolio_id', 'in': 'path', 'required': True, 'schema': {'type': 'integer'}}],
    'responses': {
        '200': {'description': 'Portfolio summary.'},
        '401': {'description': 'Unauthorized.'},
        '404': {'description': 'Portfolio not found.'}
    }
})
def get_portfolio_summary_endpoint(portfolio_id):
    try:
        # Add ownership check here if necessary, similar to get_portfolio
        summary = portfolio_service.get_portfolio_summary(portfolio_id)
        return jsonify(summary), 200
    except ValueError as e: # Catches 'Portfolio not found' from service
        return jsonify({'message': str(e)}), 404

@portfolio_bp.route('/<int:portfolio_id>/movements', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Portfolios'],
    'summary': 'Add an instrument movement (buy/sell) to a portfolio.',
    'security': [{'BearerAuth': []}],
    'parameters': [{'name': 'portfolio_id', 'in': 'path', 'required': True, 'schema': {'type': 'integer'}}],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'instrumento_simbolo': {'type': 'string', 'example': 'AAPL'},
                        'cantidad': {'type': 'number', 'example': 10},
                        'precio_unitario': {'type': 'number', 'example': 150.75},
                        'tipo_operacion': {'type': 'string', 'example': 'compra', 'enum': ['compra', 'venta']},
                        'fecha': {'type': 'string', 'format': 'date', 'example': '2023-10-26'} # Changed to date
                    },
                    'required': ['instrumento_simbolo', 'cantidad', 'precio_unitario', 'tipo_operacion']
                }
            }
        }
    },
    'responses': {
        '201': {'description': 'Movement added successfully.'},
        '400': {'description': 'Invalid input or insufficient quantity for sale.'},
        '401': {'description': 'Unauthorized.'},
        '404': {'description': 'Portfolio or Instrument not found.'}
    }
})
def add_portfolio_movement(portfolio_id):
    data = request.get_json()
    try:
        # Add ownership check here if necessary
        movement = portfolio_service.add_instrument_to_portfolio(portfolio_id, data)
        return jsonify({'message': 'Movement added', 'movement_id': movement.id}), 201
    except ValueError as e: # Catches various errors from service
        # Determine appropriate status code based on error message content
        if "not found" in str(e).lower():
            return jsonify({'message': str(e)}), 404
        else:
            return jsonify({'message': str(e)}), 400


@portfolio_bp.route('/<int:portfolio_id>/suggestions', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Portfolios'],
    'summary': 'Get investment suggestions for a portfolio.',
    'security': [{'BearerAuth': []}],
    'parameters': [{'name': 'portfolio_id', 'in': 'path', 'required': True, 'schema': {'type': 'integer'}}],
    'responses': {
        '200': {'description': 'Investment suggestions.'},
        '401': {'description': 'Unauthorized.'},
        '404': {'description': 'Portfolio not found.'}
    }
})
def get_portfolio_suggestions_endpoint(portfolio_id):
    try:
        # Add ownership check here if necessary
        suggestions = suggestion_service.generate_suggestions(portfolio_id)
        return jsonify(suggestions), 200
    except ValueError as e: # Catches 'Portfolio not found' from service
        return jsonify({'message': str(e)}), 404
