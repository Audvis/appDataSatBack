from flask import request
from controllers import download_csv, get_data, delete_all_data

def configure_routes(app):
    # Ruta principal
    @app.route('/')
    def home():
        return jsonify({'message': 'Bienvenido a la API de cancelados'})

    # Ruta para descargar el archivo CSV
    @app.route('/download_csv', methods=['GET'])
    def handle_download_csv():
        return download_csv()

    # Ruta para obtener los datos guardados en la base de datos con paginación
    @app.route('/get_data', methods=['GET'])
    def handle_get_data():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        return get_data(page, per_page)

    # Ruta para borrar todos los registros
    @app.route('/delete_all', methods=['DELETE'])
    def handle_delete_all():
        return delete_all_data()
