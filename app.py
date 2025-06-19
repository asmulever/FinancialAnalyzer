from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finanzas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======================= MODELOS =======================

class InstrumentoFinanciero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50))
    simbolo = db.Column(db.String(10))

class Cartera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    propietario = db.Column(db.String(100))

class HistoricoMovimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cartera_id = db.Column(db.Integer, db.ForeignKey('cartera.id'))
    instrumento_id = db.Column(db.Integer, db.ForeignKey('instrumento_financiero.id'))
    fecha = db.Column(db.String(20))
    cantidad = db.Column(db.Float)
    precio_unitario = db.Column(db.Float)

class MonitorAccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    simbolo = db.Column(db.String(10))
    fecha = db.Column(db.String(20))
    precio = db.Column(db.Float)

# ======================= RUTAS =======================

@app.route("/instrumentos", methods=["GET", "POST"])
def instrumentos():
    if request.method == "POST":
        data = request.get_json()
        nuevo = InstrumentoFinanciero(
            nombre=data["nombre"],
            tipo=data.get("tipo"),
            simbolo=data.get("simbolo")
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"mensaje": "Instrumento creado"}), 201

    instrumentos = InstrumentoFinanciero.query.all()
    return jsonify([
        {"id": i.id, "nombre": i.nombre, "tipo": i.tipo, "simbolo": i.simbolo}
        for i in instrumentos
    ])

@app.route("/carteras", methods=["GET", "POST"])
def carteras():
    if request.method == "POST":
        data = request.get_json()
        nueva = Cartera(nombre=data["nombre"], propietario=data.get("propietario"))
        db.session.add(nueva)
        db.session.commit()
        return jsonify({"mensaje": "Cartera creada"}), 201

    carteras = Cartera.query.all()
    return jsonify([
        {"id": c.id, "nombre": c.nombre, "propietario": c.propietario}
        for c in carteras
    ])

# ================ INIT DB ================

@app.before_first_request
def crear_tablas():
    db.create_all()

# ================ MAIN ================

if __name__ == "__main__":
    app.run(debug=True)

