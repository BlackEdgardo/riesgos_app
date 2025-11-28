# 1. Definimos la imagen base con la versión exacta que necesitas
FROM python:3.11.9-slim

# 2. Evitamos que Python genere archivos .pyc y activamos logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiamos primero los requerimientos para aprovechar la caché de Docker
COPY requirements.txt .

# 5. Instalamos las dependencias
# Nota: Usamos --no-cache-dir para mantener la imagen ligera
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos el resto del código de la aplicación
COPY . .

# 7. Comando de arranque para Render usando Gunicorn
# "wsgi:app" significa: busca el archivo wsgi.py y ejecuta el objeto 'app'
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "wsgi:app"]