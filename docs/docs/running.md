# Running Alcali

!!!info
    This page will assume you are running alcali locally.
    
    If you are using docker, just prepend commands with `docker exec -it <name>`

First make sure that Alcali is correctly installed.

You can verify installation by running:

```commandline
alcali --version
# alcali version 2019.2.1
```

You  can also check that Alcali can access `salt` database and that [needed env var](configuration.md) are set by running:

```commandline
alcali check
# db: ok
# env: ok
```

## First Run

### Apply migrations

!!!danger

    **On the first run and after every update, you need to make sure that the database is synchronized with the current set of models and migrations. If unsure, just run `alcali migrate`**


Locally:

```commandline
alcali migrate
```

### Create a super user

Run:

```commandline
alcali createsuperuser
```
You will be prompted for your desired login, email address and password.

### Collectstatic

Run:

```commandline
alcali collectstatic
```
## Run

Once migrations are applied and a super user is created, you can start the application.

Locally:

```commandline
ENV_PATH=. alcali runserver 0.0.0.0:8000
```

In a docker container:
```commandline
docker run --rm -it -p 8000:8000 --env-file=FILE latenighttales/alcali:2019.2.0
```