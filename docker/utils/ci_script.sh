#!/bin/bash

docker-compose exec -u alcali web pip install --quiet --user -r requirements/test
make ci
while ! [[ $(docker-compose logs | grep "The Salt Master has cached the public key for this node") ]];
do
    echo "Waiting Salt Master..."
    sleep 10
done
make tests
