


build:
	docker build -t schedule .
	docker run --rm --env-file .env -p 8000:80 -v ./db:/app/core/db schedule ./manage.py collectstatic --noinput
	docker run --rm --env-file .env -p 8000:80 -v ./db:/app/core/db schedule ./manage.py migrate

run:
	docker run --rm --env-file .env -p 8000:80 -v ./db:/app/core/db schedule