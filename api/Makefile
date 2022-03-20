build: clean env database migrate

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type f -name "*,cover" -delete

migrate:
	poetry run ./manage.py makemigrations
	poetry run ./manage.py migrate

server:
	poetry run ./manage.py runserver 0.0.0.0:8000

test:
	poetry run python -m pytest --cov . $(pytest_args)

lint:
	poetry run black . --diff

format:
	poetry run black .

env:
	cp .env.example .env