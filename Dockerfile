# base image
FROM python:3.11-alpine AS build

# set working directory
WORKDIR /code

# install pipenv
RUN apk add --no-cache build-base postgresql-dev && pip install --upgrade pip && \
    pip install pipenv

# copy Pipfile and Pipfile.lock to container
COPY Pipfile Pipfile.lock ./


# install project dependencies
RUN pipenv install --system --deploy

# copy project files to container
# copy project files to container
COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# expose port for gunicorn
EXPOSE 8000

# run gunicorn
CMD ["gunicorn", "todolist.wsgi:application", "--bind", "0.0.0.0:8000"]