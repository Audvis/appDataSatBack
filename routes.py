# routes.py

from flask import Blueprint
from controllers import home, download_csv_route, get_data, delete_all

# Crear un Blueprint para las rutas
main = Blueprint('main', __name__)

# Ruta principal
main.route('/')(home)

# Ruta para descargar el archivo CSV
main.route('/download_csv', methods=['GET'])(download_csv_route)

# Ruta para obtener los datos guardados en la base de datos
main.route('/get_data', methods=['GET'])(get_data)

# Ruta para borrar todos los registros de la base de datos
main.route('/delete_all', methods=['DELETE'])(delete_all)
