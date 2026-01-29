# -----------------------------
# 1) Build stage: install Python deps
# -----------------------------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# 2) Final stage: Streamlit + Nginx
# -----------------------------
FROM python:3.11-slim

WORKDIR /app

# Copia app e dipendenze
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

# Installa Nginx
RUN apt-get update && apt-get install -y nginx && apt-get clean

# Copia configurazione Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Espone la porta
EXPOSE 8501

# Avvia Nginx + Streamlit
CMD service nginx start && streamlit run app.py --server.port=8501 --server.address=0.0.0.0
