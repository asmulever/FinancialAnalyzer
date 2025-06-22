from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_migrate import Migrate
from app.config.config import Config

db = SQLAlchemy()
jwt = JWTManager()
swagger = Swagger()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # ─── Configuración ─────────────────────────────────────────────────────────
    app.config.from_object(Config)
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY')
    app.config['SWAGGER'] = {
        'title': 'Financial Analysis API',
        'uiversion': 3,
        'openapi': '3.0.2',
        'description': 'API for managing financial portfolios, analyzing instruments, and getting suggestions.',
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

    # ─── Inicialización de extensiones ────────────────────────────────────────
    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)
    migrate.init_app(app, db)

    # ─── Importar modelos (necesario para migraciones) ────────────────────────
    from app.models import models

    # ─── Registro de Blueprints ───────────────────────────────────────────────
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from app.controllers.financial_instrument_controller import instrument_bp
    app.register_blueprint(instrument_bp)

    from app.controllers.portfolio_controller import portfolio_bp
    app.register_blueprint(portfolio_bp)

    # ─── Base de datos inicial (solo para SQLite) ─────────────────────────────
    with app.app_context():
        if app.config.get('SQLALCHEMY_DATABASE_URI', '').startswith('sqlite'):
            db.create_all()

    # ─── Ruta raíz por defecto ────────────────────────────────────────────────
    @app.route('/')
    def index():
        return {
            'status': 'ok',
            'message': 'Financial API está en ejecución'
        }

    return app
