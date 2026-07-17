FROM python:3.13-slim

WORKDIR /code

# System deps needed to build psycopg2 if a wheel isn't available for the arch
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./APP ./APP

EXPOSE 8000

CMD ["uvicorn", "APP.main:app", "--host", "0.0.0.0", "--port", "8000"]
