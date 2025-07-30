FROM python:3.9-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar el código
COPY . .

# Exponer el puerto
EXPOSE 5000

# Ejecutamos la precarga de los modelos
COPY preload.py .

RUN python preload.py

# Comando para iniciar la app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]