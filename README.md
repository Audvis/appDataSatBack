. Backend - README.md
markdown
Copiar
# Backend de la Aplicación de Cancelados

## Descripción

Este es el backend de la aplicación de cancelados, donde se gestionan los datos relacionados con las cancelaciones. La aplicación permite:
- Descargar un archivo CSV desde una URL y guardarlo en la base de datos.
- Obtener los registros de cancelaciones con paginación.
- Eliminar todos los registros de la base de datos.

## Requisitos

- Python 3.x
- Flask
- SQLAlchemy
- Pandas
- SQLite (opcional: puede usarse otra base de datos)

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone hhttps://github.com/Audvis/appDataSatBack.git
Navegar a la carpeta del proyecto:

bash
Copiar
cd backend
Crear un entorno virtual (opcional, pero recomendado):

bash
Copiar
python3 -m venv venv
source venv/bin/activate  # Para Linux/Mac
venv\Scripts\activate     # Para Windows
Instalar las dependencias:

bash
Copiar
pip install -r requirements.txt
Ejecución
Configurar las variables de entorno (si es necesario, por ejemplo, para la base de datos):

Crea un archivo .env y configura las variables necesarias (si usas una base de datos diferente a SQLite, asegúrate de configurarlo correctamente).
Ejecutar la aplicación:

bash
Copiar
python app.py
La aplicación estará disponible en http://127.0.0.1:5000.

Endpoints

GET /download_csv: Descarga un archivo CSV desde una URL y guarda los datos en la base de datos.

GET /get_data: Obtiene los registros de la base de datos con paginación.

DELETE /delete_all: Elimina todos los registros de la base de datos.

Notas
Se está utilizando SQLite por defecto como base de datos.
Si deseas cambiar la base de datos, actualiza la URL de conexión en el archivo app.py.

Este backend está construido con Flask y utiliza SQLAlchemy para interactuar con la base de datos.
Licencia
Este proyecto está bajo la Licencia MIT.