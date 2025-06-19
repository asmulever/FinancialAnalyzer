# app/controllers/auth_controller.py
from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from flasgger import swag_from

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Register a new user.',
    'requestBody': {
        'description': 'User registration details.',
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'username': {'type': 'string', 'example': 'newuser'},
                        'email': {'type': 'string', 'example': 'newuser@example.com'},
                        'password': {'type': 'string', 'example': 'strongpassword'}
                    },
                    'required': ['username', 'email', 'password']
                }
            }
        }
    },
    'responses': {
        '201': {'description': 'User created successfully.'},
        '400': {'description': 'Invalid input (e.g., missing fields, user already exists).'},
        '500': {'description': 'Could not create user.'}
    }
})
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'message': 'Missing username, email, or password'}), 400
    try:
        user = auth_service.register_user(data)
        return jsonify({'message': f'User {user.username} created successfully'}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Could not create user', 'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Log in an existing user.',
    'requestBody': {
        'description': 'User login credentials.',
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'username': {'type': 'string', 'example': 'testuser'},
                        'password': {'type': 'string', 'example': 'password123'}
                    },
                    'required': ['username', 'password']
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Login successful, returns JWT token.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'access_token': {'type': 'string'}
                        }
                    }
                }
            }
        },
        '400': {'description': 'Missing username or password.'},
        '401': {'description': 'Invalid username or password.'},
        '500': {'description': 'Login failed.'}
    }
})
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    try:
        token = auth_service.login_user(data)
        return jsonify(token), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 401
    except Exception as e:
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500
