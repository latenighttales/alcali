#!/usr/bin/env bash

# Wait for web
echo "Waiting for web"
./wait-for web:8000

exec "$@"