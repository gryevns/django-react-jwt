# Django/React Template

Django & ReactJS template using docker-compose for local development.

## Features

- Poetry
- Postgres
- JWT Authentication
- Tailwind CSS

## Usage

```sh
# start api/react/postgres services
docker compose up

# create a superuser
docker-compose exec api bash
poetry run python ./manage.py createsuperuser

# visit react app at http://localhost:3000 & login with username/password
```
