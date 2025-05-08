#!/bin/bash
set -eo pipefail

echo "Checking if netcat is installed..."
which nc || echo "Netcat is NOT installed!"

echo "Installing Netcat..."
/bin/bash
apt update && apt-get install -y netcat-traditional

echo "Waiting for MySQL to start..."
while ! /usr/bin/nc -z db 3306; do
  echo "Waiting for MySQL..."
  sleep 2  # Increase delay if necessary
done
echo "MySQL is up!"

python manage.py seed_users  # Seeds users to auth_users
python manage.py seed_documents
python manage.py seed_images

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
#python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 cirtwebsite.wsgi:application