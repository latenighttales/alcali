#!/bin/bash

while ! [[ $(docker-compose logs | grep "The Salt Master has cached the public key for this node") ]];
do
    echo "Waiting Salt Master..."
    sleep 20
done
docker-compose exec -u alcali web pip install --user -r requirements/test
make tests
