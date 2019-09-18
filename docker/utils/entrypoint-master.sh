#!/usr/bin/env bash

# Wait for web
echo "Waiting for web"
./wait-for -t 60 web:8000

exec "$@"