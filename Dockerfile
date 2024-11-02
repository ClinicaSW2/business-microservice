# Dockerfile

# Usa una imagen base de Python
FROM python:3.10

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos requeridos
COPY . /app

# Instala las dependencias de Python, incluyendo Gunicorn
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# Expone el puerto para Flask (Gunicorn usará el mismo puerto)
EXPOSE 5000

# Comando de inicio usando Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
