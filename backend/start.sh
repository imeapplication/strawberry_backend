#!/bin/bash
# Wait for postgres
echo "Waiting for postgres..."
sleep 5

# Run migrations
python manage.py makemigrations core
python manage.py migrate

# Create superuser if not exists
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=admin@example.com \
DJANGO_SUPERUSER_PASSWORD=adminpassword \
python manage.py createsuperuser --noinput || true

# Create sample data (optional)
# python setup_db.py --with-sample-data

# Run server
python manage.py runserver 0.0.0.0:8000

