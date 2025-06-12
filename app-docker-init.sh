#!/bin/bash

while ! python manage.py check; do
    echo "Checks failed, waiting for the database to be ready..."
    sleep 3
done

while ! python manage.py makemigrations; do
    echo "Trying to migrate the database"
    sleep 3
done

while ! python manage.py migrate; do
    echo "Trying to migrate the database"
    sleep 3
done

echo "Django container is configured."

exec "$@"