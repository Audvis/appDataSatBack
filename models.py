# models.py

def get_db():
    from app import db
    return db

class Cancelado(get_db().Model):  # Usamos la función para obtener db
    id = get_db().Column(get_db().Integer, primary_key=True)
    RFC = get_db().Column(get_db().String(100))
    RAZON_SOCIAL = get_db().Column(get_db().String(255))
    TIPO_PERSONA = get_db().Column(get_db().String(50))
    SUPUESTO = get_db().Column(get_db().String(100))
    FECHA_CANCELACION = get_db().Column(get_db().String(50))
    MONTO = get_db().Column(get_db().String(50))
    FECHA_PUBLICACION = get_db().Column(get_db().String(50))
    ENTIDAD_FEDERATIVA = get_db().Column(get_db().String(100))
