#!/usr/bin/env bash

# Wait for database
echo "Waiting for $DB_HOST"
./docker/utils/wait-for $DB_HOST:$DB_PORT

# Migrate database and create default user
python alcali/manage.py migrate
python alcali/manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').count() or User.objects.create_superuser('admin', 'admin@example.com', 'password')"

exec "$@"
