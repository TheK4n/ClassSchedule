FROM python:3.12-alpine

EXPOSE 80

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements/prod.txt requirements/prod.txt

RUN apk --no-cache add curl && \
    pip install --no-cache-dir -r requirements/prod.txt

COPY . .

HEALTHCHECK --interval=5s --timeout=10s --retries=3 CMD curl -sS --fail 127.0.0.1:80/ping

ENTRYPOINT ["gunicorn", "core.wsgi:application", "-b", "0.0.0.0:80", "-w"]
CMD ["1"]