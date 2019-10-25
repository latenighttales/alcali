# Configuration

## Configure Alcali

If you used the [formula](https://github.com/latenighttales/alcali-formula) to install alcali, you should use the pillar to set those environment variable.

### `DB_BACKEND`

Must either be set to `mysql` or `postgresql` depending on your database choice.

### `DB_NAME`

Must always be set to `salt`.

### `DB_USER`

The username used to connect to the salt database.

### `DB_PASS`

The password used to connect to the salt database.

### `DB_HOST`

Either the hostname or the IP used to connect to the salt database.

### `DB_PORT`

By default 3306 for Mysql or 5432 for Postgres.

### `SECRET_KEY`

Used to provide cryptographic signing, and should be set to a unique, unpredictable value.

### `ALLOWED_HOSTS`

Values in this list can be fully qualified names (e.g. 'www.example.com'), in which case they will be matched against the request’s Host header exactly (case-insensitive, not including port).

A value beginning with a period can be used as a subdomain wildcard: '.example.com' will match example.com, www.example.com, and any other subdomain of example.com. A value of '*' will match anything.

### `MASTER_MINION_ID`

Salt master's minion id. leave empty if not managed.

### `SALT_URL`

The salt-api url.

Must be formed with protocol, host and port (e.g. 'https://localhost:8080')

###`SALT_AUTH`

How you choose to [authenticate](installation.md#authentication) to the salt-api.

Must be set to  `rest` or `alcali`.

## LDAP configuration

Please refer to django-auth-ldap [documentation reference](https://django-auth-ldap.readthedocs.io/en/latest/reference.html).

Here is a list of the supported settings:

- AUTH_LDAP_SERVER_URI
- AUTH_LDAP_BIND_DN
- AUTH_LDAP_BIND_PASSWORD
- AUTH_LDAP_USER_DN_TEMPLATE
- AUTH_LDAP_REQUIRE_GROUP
- AUTH_LDAP_DENY_GROUP
- AUTH_LDAP_START_TLS

### search/bind and direct bind

If you set `AUTH_LDAP_USER_DN_TEMPLATE` the search phase will be skipped.

Otherwise, you can set the search base cn with:

`AUTH_LDAP_USER_BASE_CN` 

and the search filter with:

`AUTH_LDAP_USER_SEARCH_FILTER` default: `"(objectClass=*)"`

see next for an example.

### Attribute mapping

Here is the default attribute mapping and the env var to use to override them:

```python
# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "username": os.environ.get("AUTH_LDAP_USER_ATTR_MAP_USERNAME", "sAMAccountName"),
    "first_name": os.environ.get("AUTH_LDAP_USER_ATTR_MAP_FIRST_NAME", "givenName"),
    "last_name": os.environ.get("AUTH_LDAP_USER_ATTR_MAP_LAST_NAME", "sn"),
    "email": os.environ.get("AUTH_LDAP_USER_ATTR_MAP_EMAIL", "mail"),
}
```


## `.env` file example:

```bash
DB_BACKEND=mysql
DB_NAME=salt
DB_USER=alcali
DB_PASS=alcali
DB_HOST=db
DB_PORT=3306

SECRET_KEY=thisisnotagoodsecret.orisit?
ALLOWED_HOSTS=*
MASTER_MINION_ID=master

SALT_URL=https://localhost:8080
SALT_AUTH=alcali
```

If you want to use LDAP authentication, you'll also need:

```bash
AUTH_BACKEND=ldap
AUTH_LDAP_SERVER_URI=ldap://ldap-server
AUTH_LDAP_BIND_DN=cn=admin,dc=example,dc=org
AUTH_LDAP_BIND_PASSWORD=admin
AUTH_LDAP_USER_BASE_CN=dc=example,dc=org
AUTH_LDAP_USER_SEARCH_FILTER=(uid=%(user)s)
```

## Docker

You can pass the `.env` file to the `docker run` command with the `--env-file=FILE` option.

See [running Alcali](running.md).

## Running locally

Use the `ENV_PATH` environment variable.

Example:
```commandline
# Assuming the .env file is in /opt/alcali
ENV_PATH=/opt/alcali /opt/alcali/.venv/bin/gunicorn config.wsgi:application -b 127.0.0.1:8000 -w 3
```

See [running Alcali](running.md).

