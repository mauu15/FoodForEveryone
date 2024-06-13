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

# Crea la cartella media e copia i file media
RUN mkdir -p /app/mysite/ffe/media/
COPY mysite/ffe/media /app/mysite/ffe/media/

# Comando di avvio dell'applicazione con Gunicorn
CMD gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
