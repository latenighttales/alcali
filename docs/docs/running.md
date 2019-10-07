# Running Alcali

!!!info
    This page will assume you are running alcali locally.
    
    If you are using docker, just prepend commands with `docker exec -it <name>`

First make sure that Alcali is correctly installed.

You can verify installation by running:

```commandline
alcali current_version
# alcali version 2019.2.2
```

You  can also check that Alcali can access `salt` database and that [needed env var](configuration.md) are set and loaded by running:

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

## Run

Once migrations are applied and a super user is created, you can start the application.

Alcali use Gunicorn as a WSGI HTTP server. It is installed during the installation process of Alcali.

!!!warning
    If the .env file is not in your current directory, prepend your command with `ENV_PATH=/path/to/env_file`

If you installed Alcali from sources, at the root of the repository, run:

```commandline
gunicorn config.wsgi:application -w 4
```


If you installed Alcali using pip, run:

```commandline
gunicorn config.wsgi:application -w 4 --chdir $(alcali location)
```

In a docker container:
```commandline
docker run --rm -it -p 8000:8000 --env-file=FILE latenighttales/alcali:2019.2.2 bash -c "gunicorn config.wsgi:application -w 4 --chdir $(alcali location)"
```
Where FILE is the location of the [.env file](configuration.md)
