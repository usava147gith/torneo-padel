FROM python:3.11-slim

# Directory di lavoro
WORKDIR /app

# Installazione dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia dei file principali
COPY app.py /app/app.py
COPY styles.css /app/styles.css

# Copia delle cartelle necessarie
COPY tornei /app/tornei
COPY .streamlit /app/.streamlit
COPY static /app/static


# Variabile PORT gestita da Render
ENV PORT=$PORT

# Espone la porta dinamica
EXPOSE $PORT

# Avvio Streamlit usando la porta dinamica
CMD ["sh", "-c", "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"]
