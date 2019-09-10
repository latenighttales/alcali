#!/usr/bin/env bash

# Wait for web
echo "Waiting for web"
./wait-for -t 30 web:8000

exec "$@"