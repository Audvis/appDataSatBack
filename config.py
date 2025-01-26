# config.py

import os

class Config:
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cancelados.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de CORS
    CORS_ORIGINS = "http://localhost:3000"  # Solo permite solicitudes de localhost:3000
