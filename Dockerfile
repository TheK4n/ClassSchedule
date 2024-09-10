FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements-prod.txt .

RUN pip install --no-cache-dir -r requirements-prod.txt

COPY . .

WORKDIR /app/core

CMD ["gunicorn", "core.wsgi:application", "-b", "0.0.0.0:80"]