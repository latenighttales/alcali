# -*- coding: utf-8 -*-

"""
Provide authentication using MySQL.

When using MySQL as an authentication backend, you will need to create or
use an existing table that has a username and a password column.

To get started, create a simple table that holds just a username and
a password. The password field will hold a SHA256 checksum.

.. code-block:: sql

    CREATE TABLE `users` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `username` varchar(25) DEFAULT NULL,
      `password` varchar(70) DEFAULT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

To create a user within MySQL, execute the following statement.

.. code-block:: sql

    INSERT INTO users VALUES (NULL, 'diana', SHA2('secret', 256))

.. code-block:: yaml

    mysql_auth:
      hostname: localhost
      database: SaltStack
      username: root
      password: letmein
      auth_sql: 'SELECT username FROM users WHERE username = "{0}" AND password = SHA2("{1}", 256)'

The `auth_sql` contains the SQL that will validate a user to ensure they are
correctly authenticated. This is where you can specify other SQL queries to
authenticate users.

Enable MySQL authentication.

.. code-block:: yaml

    external_auth:
      mysql:
        damian:
          - test.*

:depends:   - MySQL-python Python module
"""

from __future__ import absolute_import
import logging
import sys
from contextlib import contextmanager

# Import 3rd-party libs
import salt.ext.six as six

log = logging.getLogger(__name__)

try:
    import MySQLdb

    HAS_MYSQL = True
except ImportError:
    HAS_MYSQL = False

__virtualname__ = "alcali"


def __virtual__():
    if HAS_MYSQL:
        return __virtualname__
    return False


def _get_options():
    """
    Returns options used for the MySQL connection.
    """

    _options = {}
    defaults = {
        "host": "salt",
        "user": "salt",
        "pass": "salt",
        "db": "salt",
        "port": 3306,
        "ssl_ca": None,
        "ssl_cert": None,
        "ssl_key": None,
    }

    for k, v in six.iteritems(defaults):
        try:
            _options[k] = __opts__["{}.{}".format("mysql", k)]
        except KeyError:
            _options[k] = v

    # post processing
    for k, v in six.iteritems(_options):
        if isinstance(v, six.string_types) and v.lower() == "none":
            # Ensure 'None' is rendered as None
            _options[k] = None
        if k == "port":
            # Ensure port is an int
            _options[k] = int(v)

    return _options


@contextmanager
def _get_serv():
    """
    Return a mysql cursor
    """
    _options = _get_options()

    log.debug("Generating new MySQL connection pool")
    try:
        # An empty ssl_options dictionary passed to MySQLdb.connect will
        # effectively connect w/o SSL.
        ssl_options = {}
        if _options.get("ssl_ca"):
            ssl_options["ca"] = _options.get("ssl_ca")
        if _options.get("ssl_cert"):
            ssl_options["cert"] = _options.get("ssl_cert")
        if _options.get("ssl_key"):
            ssl_options["key"] = _options.get("ssl_key")
        conn = MySQLdb.connect(
            host=_options.get("host"),
            user=_options.get("user"),
            passwd=_options.get("pass"),
            db=_options.get("db"),
            port=_options.get("port"),
            ssl=ssl_options,
        )

    except MySQLdb.connections.OperationalError as exc:
        raise salt.exceptions.SaltMasterError(
            "MySQL returner could not connect to database: {exc}".format(exc=exc)
        )

    cursor = conn.cursor()

    try:
        yield cursor
    except MySQLdb.DatabaseError as err:
        error = err.args
        sys.stderr.write(str(error))
        raise err


def auth(username, password):
    """
    Authenticate using a MySQL user table
    """

    with _get_serv() as cur:
        sql = "SELECT c.token FROM user_settings c INNER JOIN auth_user a ON c.user_id = a.id AND a.username = '{}'".format(
            username
        )
        cur.execute(sql)

        if cur.rowcount == 1:
            user_token = cur.fetchone()
            user_token = [i for i in user_token]
            user_token = str(user_token[0])
            if str(user_token) == str(password):
                log.debug("Alcali authentication successful")
                return True

    return False
