#!/usr/bin/env bash

mkdir /var/cache/salt/master
chown -R salt:salt /var/cache/salt

# mkdir /var/cache/salt/master/extmods
# mkdir /var/cache/salt/master/roots
salt-run saltutil.sync_all
# Wait for web
echo "Waiting for web"
./wait-for -t 60 web:8000

exec "$@"
