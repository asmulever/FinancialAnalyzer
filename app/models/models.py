from app import db
from sqlalchemy.orm import relationship
from datetime import datetime # Import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class InstrumentoFinanciero(db.Model):
    __tablename__ = 'instrumento_financiero'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    tipo = db.Column(db.String(50))  # E.g., CEDEAR, Bono, Accion
    simbolo = db.Column(db.String(20), nullable=False, unique=True)
    # Relationship to link to historical movements
    movimientos = relationship('HistoricoMovimiento', back_populates='instrumento')

    def __repr__(self):
        return f'<InstrumentoFinanciero {self.simbolo}>'

class Cartera(db.Model):
    __tablename__ = 'cartera'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    propietario = db.Column(db.String(100)) # Could be a FK to a User model later
    # Relationship to link to historical movements
    movimientos = relationship('HistoricoMovimiento', back_populates='cartera')

    def __repr__(self):
        return f'<Cartera {self.nombre}>'

class HistoricoMovimiento(db.Model):
    __tablename__ = 'historico_movimiento'
    id = db.Column(db.Integer, primary_key=True)
    cartera_id = db.Column(db.Integer, db.ForeignKey('cartera.id'), nullable=False)
    instrumento_id = db.Column(db.Integer, db.ForeignKey('instrumento_financiero.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Changed to DateTime
    cantidad = db.Column(db.Float, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    tipo_operacion = db.Column(db.String(10), nullable=False) # 'compra' o 'venta'

    cartera = relationship('Cartera', back_populates='movimientos')
    instrumento = relationship('InstrumentoFinanciero', back_populates='movimientos')

    def __repr__(self):
        return f'<HistoricoMovimiento {self.instrumento.simbolo} {self.cantidad} @ {self.precio_unitario} on {self.fecha}>'

class MonitorAccion(db.Model): # This might be better named PrecioHistoricoInstrumento or similar
    __tablename__ = 'monitor_accion'
    id = db.Column(db.Integer, primary_key=True)
    instrumento_id = db.Column(db.Integer, db.ForeignKey('instrumento_financiero.id')) # Link to InstrumentoFinanciero
    simbolo = db.Column(db.String(20)) # Denormalized for quick lookup, or could join with InstrumentoFinanciero
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Changed to DateTime
    precio_apertura = db.Column(db.Float)
    precio_cierre = db.Column(db.Float, nullable=False)
    precio_maximo = db.Column(db.Float)
    precio_minimo = db.Column(db.Float)
    volumen = db.Column(db.BigInteger)

    instrumento = relationship('InstrumentoFinanciero') # Add relationship

    def __repr__(self):
        return f'<MonitorAccion {self.simbolo} {self.precio_cierre} on {self.fecha}>'

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
