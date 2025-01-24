# routes.py
from flask import jsonify, request
from models import db, Cancelado
from utils import download_csv
from app import app  # Importa la instancia de app aquí

# Ruta principal
@app.route('/')
def home():
    return jsonify({'message': 'Bienvenido a la API de cancelados'})

# Ruta para descargar el archivo CSV
@app.route('/download_csv', methods=['GET'])
def download_csv_route():
    try:
        df = download_csv()

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
