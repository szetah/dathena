#!/bin/sh

# wait for PSQL server to start
sleep 20

# prepare init migration
su -m myuser -c "python3 manage.py makemigrations"

# migrate db, so we have the latest db schema
su -m myuser -c "python3 manage.py migrate"

# load initial data into documents app
su -m myuser -c "python3 manage.py loaddata document_initial_data.json"

# create a superuser if not exists
echo "from django.contrib.auth.models import User\nif not User.objects.filter(username='admin').exists():User.objects.create_superuser('admin', 'admin@example.com', 'password');" | python manage.py shell

# start development server on public ip interface, on port 8000
su -m myuser -c "python3 manage.py runserver 0.0.0.0:8000"


