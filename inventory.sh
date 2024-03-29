docker container prune -f

docker rmi $(docker images -f "dangling=true" -q) || true

docker compose up -d db

pipenv run python manage.py migrate

pipenv run python manage.py runserver 127.0.0.1:8000