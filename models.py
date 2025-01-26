# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
