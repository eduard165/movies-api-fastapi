# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de configuración, incluyendo .env y requirements.txt
COPY requirements.txt ./
COPY .env ./

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de la carpeta `app` al directorio de trabajo
COPY app/ /app/app/

# Copia cualquier otro archivo necesario como `config.py`
COPY . /app/

# Expone el puerto que la aplicación usará (por ejemplo, 8000 para FastAPI)
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
