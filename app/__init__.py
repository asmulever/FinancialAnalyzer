from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_migrate import Migrate # New import for Flask-Migrate
from app.config.config import Config

db = SQLAlchemy()
jwt = JWTManager()
swagger = Swagger()
migrate = Migrate() # New Migrate instance

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY')
    app.config['SWAGGER'] = {
        'title': 'Financial Analysis API',
        'uiversion': 3,
        'openapi': '3.0.2',
        'description': 'API for managing financial portfolios, analyzing instruments, and getting suggestions.',
        'termsOfService': None,
        'contact': {
            'name': 'API Support',
            'email': 'support@example.com'
        },
        'license': {
            'name': 'MIT',
            'url': 'https://opensource.org/licenses/MIT'
        },
        'components': {
            'securitySchemes': {
                'BearerAuth': {
                    'type': 'http',
                    'scheme': 'bearer',
                    'bearerFormat': 'JWT'
                }
            }
        },
        'security': [{'BearerAuth': []}]
    }

    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)
    migrate.init_app(app, db) # Initialize Migrate

    from app.models import models # Ensure models are imported for db.create_all() and migrations

    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from app.controllers.financial_instrument_controller import instrument_bp
    app.register_blueprint(instrument_bp)

    from app.controllers.portfolio_controller import portfolio_bp
    app.register_blueprint(portfolio_bp)

    with app.app_context():
        # db.create_all() # We'll let Flask-Migrate handle table creation from now on, or use it for initial setup.
        # For the very first run without existing migrations, db.create_all() can be useful.
        # However, once Flask-Migrate is in use, 'flask db upgrade' is the standard way.
        # For now, let's assume db.create_all() has done its job or will be run manually once if needed.
        # If you run 'flask db init', then 'flask db migrate', then 'flask db upgrade', create_all() is not strictly needed here.
        # To be safe for now and ensure tables exist for current execution without manual migration steps:
        if app.config.get('SQLALCHEMY_DATABASE_URI').startswith('sqlite'): # Avoid running create_all if not sqlite for safety in other DBs
             db.create_all()

    return app
