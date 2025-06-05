#!/bin/sh

python3 manage.py migrate --noinput && python3 manage.py collectstatic --noinput && uvicorn daria.asgi:application --host 0.0.0.0 --port 8000 --reload