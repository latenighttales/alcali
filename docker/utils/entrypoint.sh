#!/usr/bin/env bash

# Wait for database
echo "Waiting for $DB_HOST"
./docker/utils/wait-for $DB_HOST:$DB_PORT

echo "Database on $DB_HOST ready"

exec "$@"
