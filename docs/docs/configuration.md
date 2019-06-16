# Configuration

## Configure Alcali

### `.env` file

```bash
# alcali_backend can be set to netapi or pyapi.
ALCALI_BACKEND=netapi

MASTER_MINION_ID=master

# DB
DB_BACKEND=mysql
DB_NAME=salt
DB_USER=alcali
DB_PASS=alcali
DB_HOST=db
DB_PORT=3306

# django
DJANGO_DEBUG=true
DJANGO_SECRET=thisisnotagoodsecret.orisit?
ALLOWED_HOSTS=*
DJANGO_SETTINGS=config.settings.dev

# salt-api
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

