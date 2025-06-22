import os
from app import create_app

# Configuración de entorno opcional (puede sobrescribirse con .env o export FLASK_ENV, etc.)
os.environ.setdefault('FLASK_ENV', 'development')
os.environ.setdefault('FLASK_DEBUG', '1')

app = create_app()

if __name__ == '__main__':
    # Puedes usar os.getenv para valores externos si es necesario
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=app.config.get('DEBUG', True)
    )
