# Dockerfile

FROM python:3.10.0-slim

# Installa i pacchetti necessari
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libcairo2-dev

# Pulizia
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Imposta il workdir dell'applicazione
WORKDIR /app

# Copia il file requirements.txt e installa le dipendenze
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copia il resto del codice dell'applicazione
COPY . .

# Copia i file media nella cartella media
RUN mkdir -p /app/media/
COPY media /app/media/

# Comando di avvio dell'applicazione con Gunicorn
CMD gunicorn mysite.wsgi
