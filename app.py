# app.py
from flask import Flask
from flask_migrate import Migrate
from config import Config
from models import db
from routes import *

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración de la aplicación
app.config.from_object(Config)

# Inicializar la base de datos y migraciones
db.init_app(app)
migrate = Migrate(app, db)

# Ejecutar el servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
