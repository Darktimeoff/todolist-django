docker container prune -f

docker rmi $(docker images -f "dangling=true" -q) || true

docker compose pull

docker compose -p todolist-local up -d

pipenv run python manage.py migrate

pipenv run python manage.py runserver 127.0.0.1:8000