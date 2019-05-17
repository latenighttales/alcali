# Alcali

<img align="right" height="300" src="alcali/web/static/img/logo-1089.png">


## What's Alcali?

Alcali is a web based tool for monitoring and administrating **Saltstack®** Salt.

## Features

- Get notified in real time when a job is created, updated or has returned. 

- Store your jobs results by leveraging the `master_job_store` setting with Alcali master returner.

- Check your minions conformity to their highstate.

- Keep track of custom state at a glance.

- Use custom auth module to login into both Alcali and the Salt-api using JWT.

... and many more.

## Deploying

- On Salt master:


### Using Docker

### Manually

## Installation

### using pip:

```bash
pip install alcali
```

### From sources:

```bash
git clone https://...
```

on the salt master:

copy config

sudo apt install python-mysqldb python-pip

sudo pip install CherryPy==3.2.3

sudo apt install salt-api

sudo systemctl restart salt-api

CREATE DATABASE salt;

CREATE USER 'mysql'@'*' IDENTIFIED BY 'mysql';

GRANT ALL PRIVILEGES ON * . * TO 'mysql'@'*';

FLUSH PRIVILEGES;

sudo vi /etc/mysql/mariadb.conf.d/50-server.cnf  # bind-address

sudo systemctl restart mysql


on alcali:

(virtualenv) pip install -r requirements/prod

cd alcali

./manage.py migrate

./manage.py alcali --init 

## Usage

```bash
alcali init_db && alcali runserver
```

## Documentation

## Licence

[MIT](LICENSE)

## Contributing

If you'd like to contribute, simply fork the repository, commit your changes, run the tests and send a pull request.