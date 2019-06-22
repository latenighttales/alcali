# Configuration

## Configure Alcali

### `.env` file

```bash
# Database settings.
DB_BACKEND=mysql # Options are: mysql or postgresql
DB_NAME=salt
DB_USER=alcali
DB_PASS=alcali
DB_HOST=db # Either hostname or ip
DB_PORT=3306 # By default 3306 for Mysql or 5432 for Postgres

# Alcali settings.
SECRET_KEY=thisisnotagoodsecret.orisit? # Used to secure signed data.
ALLOWED_HOSTS=*
MASTER_MINION_ID=master # Master's minion id.


# salt-api settings.
SALT_USER=admin
SALT_PASS=testytest
SALT_URL=https://localhost:8080
SALT_AUTH=alcali
```

Use this as an example.

## Docker

You can pass the `.env` file to the `docker run` command with the `--env-file=FILE` option.

See [running Alcali](running.md).

## Running locally

Use the `ENV_PATH` environment variable.

See [running Alcali](running.md).

