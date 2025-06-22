# 📊 FinancialAnalyzer

Aplicación web para la gestión y visualización de stock, movimientos de productos y predicciones de ventas, construida con Flask en el backend y React + Vite en el frontend.

---

## 🧱 Estructura del Proyecto

FinancialAnalyzer/
│
├── backend/ # API REST en Flask + SQLAlchemy
│ ├── app/
│ ├── instance/
│ ├── run.py
│ ├── requirements.txt
│ └── .venv/
│
├── frontend/ # Interfaz SPA en React + Material UI
│ ├── public/
│ ├── src/
│ ├── package.json
│ └── vite.config.js
│
├── README.md
└── LICENSE

#YAML


---

## 🚀 Instalación

### Requisitos
- Node.js v18+
- Python 3.10+
- npm
- pip
- (Opcional) Docker + Docker Compose

---

### 1. Backend (Flask)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py

