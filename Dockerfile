FROM python:3.11-slim

# Cartella di lavoro
WORKDIR /app

# Installazione dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia dei file dell'app
COPY app.py /app/app.py
COPY styles.css /app/styles.css

# Copia delle cartelle necessarie
COPY icons /app/icons
COPY tornei /app/tornei
COPY .streamlit /app/.streamlit

# Porta usata da Streamlit
ENV PORT=10000
EXPOSE 10000

# Avvio dell'app
CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]
