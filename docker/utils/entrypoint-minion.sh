#!/usr/bin/env bash

# Assign hostname as minion id.
echo `hostname`>/etc/salt/minion_id

exec "$@"