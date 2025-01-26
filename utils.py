# utils.py

import requests
import pandas as pd
from io import BytesIO

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

        return df

    except Exception as e:
        print(f"Error: {e}")
        raise
