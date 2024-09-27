FROM python:slim

ARG PORT=8080
ARG USER_=python

EXPOSE $PORT

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd -g 10001 $USER_ && \
   useradd -M -s /bin/false -u 10000 -g $USER_ $USER_

COPY --chown=$USER_:$USER_ requirements/prod.txt requirements-prod.txt

RUN pip install --no-cache-dir -r requirements-prod.txt

COPY --chown=$USER_:$USER_ . .

ENTRYPOINT ["./entrypoint.sh", "python", "8080"]
CMD ["1"]