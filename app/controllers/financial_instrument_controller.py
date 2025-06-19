# app/controllers/financial_instrument_controller.py
from flask import Blueprint, request, jsonify
from app.services.financial_instrument_service import FinancialInstrumentService
from app.services.analysis_service import AnalysisService
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity

instrument_bp = Blueprint('instruments', __name__, url_prefix='/instruments')
instrument_service = FinancialInstrumentService()
analysis_service = AnalysisService()

@instrument_bp.route('/', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Financial Instruments'],
    'summary': 'Create a new financial instrument.',
    'security': [{'BearerAuth': []}],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'nombre': {'type': 'string', 'example': 'Bitcoin'},
                        'tipo': {'type': 'string', 'example': 'Criptomoneda'},
                        'simbolo': {'type': 'string', 'example': 'BTCUSD'}
                    },
                    'required': ['nombre', 'simbolo', 'tipo']
                }
            }
        }
    },
    'responses': {
        '201': {'description': 'Instrument created successfully.'},
        '400': {'description': 'Invalid input or instrument already exists.'},
        '401': {'description': 'Unauthorized.'}
    }
})
def create_instrument():
    data = request.get_json()
    try:
        instrument = instrument_service.create_instrument(data)
        return jsonify({'message': 'Instrument created successfully', 'instrument': {'id': instrument.id, 'nombre': instrument.nombre, 'simbolo': instrument.simbolo, 'tipo': instrument.tipo}}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@instrument_bp.route('/', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Financial Instruments'],
    'summary': 'Get all financial instruments.',
    'security': [{'BearerAuth': []}],
    'responses': {
        '200': {'description': 'List of instruments.'},
        '401': {'description': 'Unauthorized.'}
    }
})
def get_all_instruments():
    instruments = instrument_service.get_all_instruments()
    return jsonify([{'id': i.id, 'nombre': i.nombre, 'tipo': i.tipo, 'simbolo': i.simbolo} for i in instruments]), 200

@instrument_bp.route('/<string:instrument_id_or_symbol>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Financial Instruments'],
    'summary': 'Get a specific financial instrument by ID or symbol.',
    'security': [{'BearerAuth': []}],
    'parameters': [
        {'name': 'instrument_id_or_symbol', 'in': 'path', 'required': True, 'description': 'ID or symbol of the instrument', 'schema': {'type': 'string'}}
    ],
    'responses': {
        '200': {'description': 'Instrument details.'},
        '401': {'description': 'Unauthorized.'},
        '404': {'description': 'Instrument not found.'}
    }
})
def get_instrument(instrument_id_or_symbol):
    try:
        instrument_id = int(instrument_id_or_symbol)
        instrument = instrument_service.get_instrument_by_id(instrument_id)
    except ValueError: # Not an integer, so it's a symbol
        instrument = instrument_service.get_instrument_by_symbol(instrument_id_or_symbol)
    if not instrument:
        return jsonify({'message': 'Instrument not found'}), 404
    return jsonify({'id': instrument.id, 'nombre': instrument.nombre, 'tipo': instrument.tipo, 'simbolo': instrument.simbolo}), 200

@instrument_bp.route('/<string:instrument_id_or_symbol>/analysis', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Financial Instruments'],
    'summary': 'Get analysis for a specific financial instrument.',
    'security': [{'BearerAuth': []}],
    'parameters': [
        {'name': 'instrument_id_or_symbol', 'in': 'path', 'required': True, 'description': 'ID or symbol of the instrument for analysis.', 'schema': {'type': 'string'}}
    ],
    'responses': {
        '200': {'description': 'Instrument analysis results.'},
        '401': {'description': 'Unauthorized.'},
        '404': {'description': 'Instrument not found.'}
    }
})
def get_instrument_analysis_endpoint(instrument_id_or_symbol):
    try:
        # Determine if it's an ID (integer) or symbol (string)
        try:
            param = int(instrument_id_or_symbol)
        except ValueError:
            param = instrument_id_or_symbol
        analysis = analysis_service.get_instrument_analysis(param)
        return jsonify(analysis), 200
    except ValueError as e: # Catches 'Instrument not found' from service
        return jsonify({'message': str(e)}), 404
