FROM python:3.14-slim

# Evitando que o Python escreva arquivos .pyc e garantindo que os logs saiam em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


# Instalando dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
