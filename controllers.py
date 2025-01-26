# src/backend/controllers.py
from flask import jsonify, request
from models import db, Cancelado
from utils import download_csv

def home():
    return jsonify({'message': 'Bienvenido a la API de cancelados'})

def download_csv_route():
    try:
        # Descargar y leer el CSV
        df = download_csv()

        # Verificar si las columnas necesarias están presentes
        if 'RFC' not in df.columns or 'RAZÓN SOCIAL' not in df.columns or 'MONTO' not in df.columns:
            return jsonify({'success': False, 'message': 'Las columnas necesarias no están en el archivo CSV'})

        # Crear una lista de objetos Cancelado para insertar en la base de datos
        cancelados_to_insert = []
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
            cancelados_to_insert.append(cancelado)

        # Realizar la inserción en bloque para mejorar el rendimiento
        db.session.bulk_save_objects(cancelados_to_insert)  # Inserción en bloque
        db.session.commit()  # Confirmar la transacción solo una vez al final

        return jsonify({'success': True, 'message': 'Datos guardados correctamente en la base de datos'})

    except Exception as e:
        db.session.rollback()  # En caso de error, revertir los cambios
        return jsonify({'success': False, 'message': f'Hubo un problema al descargar o guardar el archivo: {e}'})


def get_data():
    try:
        # Obtener parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)

        # Obtener los registros paginados
        cancelados = Cancelado.query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Crear la respuesta con los registros obtenidos
        result = []
        for cancelado in cancelados.items:
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
        
        # Obtener el total de registros y total de páginas
        total_count = Cancelado.query.count()  # Número total de registros
        return jsonify({
            'data': result,
            'total_count': total_count,  # Incluir el total de registros
            'total_pages': cancelados.pages  # Incluir el total de páginas
        })

    except Exception as e:
        return jsonify({'message': f'Hubo un problema al obtener los datos: {str(e)}', 'success': False})


def delete_all():
    try:
        # Borrar todos los registros de la tabla
        db.session.query(Cancelado).delete()
        db.session.commit()  # Confirmar la transacción

        return jsonify({'success': True, 'message': 'Todos los registros han sido eliminados correctamente'})

    except Exception as e:
        db.session.rollback()  # En caso de error, revertir los cambios
        return jsonify({'success': False, 'message': f'Hubo un problema al eliminar los datos: {str(e)}'})
