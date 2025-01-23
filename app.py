import os
import requests
import pandas as pd
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from flask_migrate import Migrate

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos (SQLite en este caso)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cancelados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configuración de Flask-Migrate para manejar migraciones
migrate = Migrate(app, db)

# Definir el modelo de la base de datos
class Cancelado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    RFC = db.Column(db.String(100))
    RAZON_SOCIAL = db.Column(db.String(255))
    TIPO_PERSONA = db.Column(db.String(50))
    SUPUESTO = db.Column(db.String(100))
    FECHA_CANCELACION = db.Column(db.String(50))
    MONTO = db.Column(db.String(50))
    FECHA_PUBLICACION = db.Column(db.String(50))
    ENTIDAD_FEDERATIVA = db.Column(db.String(100))

# Ruta principal
@app.route('/')
def home():
    return jsonify({'message': 'Bienvenido a la API de cancelados'})

# Ruta para descargar el archivo CSV
@app.route('/download_csv', methods=['GET'])
def download_csv():
    try:
        # URL del archivo CSV en la web
        url = 'http://omawww.sat.gob.mx/cifras_sat/Documents/Cancelados.csv'

        # Descargar el archivo CSV desde la URL
        print("Descargando archivo...")
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la descarga falla
        print("Archivo descargado correctamente")

        # Crear un objeto en memoria (BytesIO) para devolver el archivo sin necesidad de guardarlo en disco
        file_bytes = BytesIO(response.content)

        # Usar pandas para leer el archivo CSV con una codificación diferente
        print("Leyendo archivo CSV...")
        df = pd.read_csv(file_bytes, encoding='ISO-8859-1')  # Usamos la codificación ISO-8859-1
        print(f"Columnas encontradas en el CSV: {df.columns.tolist()}")  # Imprimir las columnas del archivo
        print(f"Primeras filas del archivo CSV:\n{df.head()}")  # Imprimir las primeras filas del archivo CSV

        # Eliminar espacios en blanco en los nombres de las columnas
        df.columns = df.columns.str.strip()

        # Verificar que las columnas necesarias están presentes en el archivo
        if 'RFC' not in df.columns or 'RAZÓN SOCIAL' not in df.columns or 'MONTO' not in df.columns:
            print("Error: No se encontraron las columnas necesarias en el CSV.")
            return jsonify({'success': False, 'message': 'Las columnas necesarias no están en el archivo CSV'})

        # Guardar cada fila del CSV en la base de datos
        for index, row in df.iterrows():
            cancelado = Cancelado(
                RFC=row['RFC'],
                RAZON_SOCIAL=row['RAZÓN SOCIAL'],
                TIPO_PERSONA=row['TIPO PERSONA'],
                SUPUESTO=row['SUPUESTO'],
                FECHA_CANCELACION=row['FECHA DE CANCELACIÓN'],
                MONTO=row['MONTO'],  
                FECHA_PUBLICACION=row['FECHA DE PUBLICACIÓN'],
                ENTIDAD_FEDERATIVA=row['ENTIDAD FEDERATIVA']
            )
            db.session.add(cancelado)

        db.session.commit()  # Confirmar la transacción
        print("Datos guardados correctamente en la base de datos")

        return jsonify({'success': True, 'message': 'Datos guardados correctamente en la base de datos'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': f'Hubo un problema al descargar o guardar el archivo: {e}'})


# Ruta para obtener los datos guardados en la base de datos
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        # Obtener parámetros de paginación (por ejemplo, página y límite de registros por página)
        page = request.args.get('page', 1, type=int)  # Página actual (por defecto es 1)
        per_page = request.args.get('per_page', 50, type=int)  # Registros por página (por defecto es 50)

        # Consultar los registros con paginación
        cancelados = Cancelado.query.paginate(page=page, per_page=per_page, error_out=False).items

        # Crear una lista de diccionarios con los resultados
        result = []
        for cancelado in cancelados:
            result.append({
                'id': cancelado.id,
                'RFC': cancelado.RFC,
                'RAZON_SOCIAL': cancelado.RAZON_SOCIAL,
                'TIPO_PERSONA': cancelado.TIPO_PERSONA,
                'SUPUESTO': cancelado.SUPUESTO,
                'FECHA_CANCELACION': cancelado.FECHA_CANCELACION,
                'MONTO': cancelado.MONTO,
                'FECHA_PUBLICACION': cancelado.FECHA_PUBLICACION,
                'ENTIDAD_FEDERATIVA': cancelado.ENTIDAD_FEDERATIVA
            })

        # Devolver los datos como respuesta JSON
        return jsonify(result)

    except Exception as e:
        # Manejo de errores
        return jsonify({'message': f'Hubo un problema al obtener los datos: {str(e)}', 'success': False})


# Ejecutar el servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
