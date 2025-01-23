from models import Cancelado
from app import db
import requests
import pandas as pd
from io import BytesIO
from flask import jsonify

# Función para descargar y guardar el CSV
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
        df = pd.read_csv(file_bytes, encoding='ISO-8859-1')
        print(f"Columnas encontradas en el CSV: {df.columns.tolist()}")

        # Eliminar espacios en blanco en los nombres de las columnas
        df.columns = df.columns.str.strip()

        # Verificar que las columnas necesarias están presentes en el archivo
        if 'RFC' not in df.columns or 'RAZÓN SOCIAL' not in df.columns or 'MONTO' not in df.columns:
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


# Función para obtener los datos guardados en la base de datos
def get_data(page, per_page):
    try:
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


# Función para borrar todos los registros de la base de datos
def delete_all_data():
    try:
        # Borrar todos los registros de la tabla
        db.session.query(Cancelado).delete()
        db.session.commit()
        return jsonify({'success': True, 'message': 'Todos los registros han sido eliminados correctamente'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Hubo un problema al eliminar los datos: {str(e)}'})
