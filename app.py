# app.py

from flask import Flask
from flask_migrate import Migrate
from config import Config
from models import db
from routes import main
from flask_cors import CORS  # Importar CORS

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración de la aplicación
app.config.from_object(Config)

# Configura CORS utilizando la opción de configuración en config.py
CORS(app, origins=app.config['CORS_ORIGINS'])  # Obtén CORS_ORIGINS desde la configuración

# Inicializar la base de datos y migraciones
db.init_app(app)
migrate = Migrate(app, db)

# Registrar las rutas del blueprint
app.register_blueprint(main)

# Ejecutar el servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
