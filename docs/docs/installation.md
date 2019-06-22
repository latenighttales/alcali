# Installation

## Prerequisite

- A database (**MariaDB/Mysql** or **Postgres**) accessible to both your Salt master and Alcali.
- the [Salt-Api](https://docs.saltstack.com/en/latest/ref/cli/salt-api.html#salt-api) installed and accessible by Alcali.

![structure](images/structure.png)

 

## Preparing the salt master

### Database access and master job store configuration

The salt master needs to store its jobs on the chosen database.

!!!warning
    
    Don't forget to install database connectors:
    
     - `python-mysqldb/python3-mysqldb` for MySQL/MariaDB
     - `python-psycopg2/python3-psycopg2` for Postgres
     
<details><summary>MySQL/MariaDB schema and configuration example</summary>
<p>

```sql
CREATE DATABASE  `salt`
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;

USE `salt`;

--
-- Table structure for table `jids`
--

DROP TABLE IF EXISTS `jids`;
CREATE TABLE `jids` (
  `jid` varchar(255) NOT NULL,
  `load` mediumtext NOT NULL,
  UNIQUE KEY `jid` (`jid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `salt_returns`
--

DROP TABLE IF EXISTS `salt_returns`;
CREATE TABLE `salt_returns` (
  `fun` varchar(50) NOT NULL,
  `jid` varchar(255) NOT NULL,
  `return` mediumtext NOT NULL,
  `id` varchar(255) NOT NULL,
  `success` varchar(10) NOT NULL,
  `full_ret` mediumtext NOT NULL,
  `alter_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`),
  KEY `jid` (`jid`),
  KEY `fun` (`fun`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `salt_events`
--

DROP TABLE IF EXISTS `salt_events`;
CREATE TABLE `salt_events` (
`id` BIGINT NOT NULL AUTO_INCREMENT,
`tag` varchar(255) NOT NULL,
`data` mediumtext NOT NULL,
`alter_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
`master_id` varchar(255) NOT NULL,
PRIMARY KEY (`id`),
KEY `tag` (`tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

Salt master configuration example:

```yaml
event_return: [mysql]
master_job_cache: mysql
mysql.host: 'db'
mysql.user: 'alcali'
mysql.pass: 'alcali'
mysql.db: 'salt'
mysql.port: 3306
``` 

</p>
</details>

<details><summary>Postgres commands and configuration example</summary>
<p>

```sql
psql << EOF
CREATE ROLE salt WITH PASSWORD 'salt';
CREATE DATABASE salt WITH OWNER salt;
EOF

psql -h localhost -U salt << EOF
--
-- Table structure for table 'jids'
--

DROP TABLE IF EXISTS jids;
CREATE TABLE jids (
  jid   varchar(20) PRIMARY KEY,
  load  text NOT NULL
);

--
-- Table structure for table 'salt_returns'
--

DROP TABLE IF EXISTS salt_returns;
CREATE TABLE salt_returns (
  fun       varchar(50) NOT NULL,
  jid       varchar(255) NOT NULL,
  return    text NOT NULL,
  full_ret  text,
  id        varchar(255) NOT NULL,
  success   varchar(10) NOT NULL,
  alter_time   TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_salt_returns_id ON salt_returns (id);
CREATE INDEX idx_salt_returns_jid ON salt_returns (jid);
CREATE INDEX idx_salt_returns_fun ON salt_returns (fun);
CREATE INDEX idx_salt_returns_updated ON salt_returns (alter_time);

--
-- Table structure for table 'salt_events'
--

DROP TABLE IF EXISTS salt_events;
DROP SEQUENCE IF EXISTS seq_salt_events_id;
CREATE SEQUENCE seq_salt_events_id;
CREATE TABLE salt_events (
    id BIGINT NOT NULL UNIQUE DEFAULT nextval('seq_salt_events_id'),
    tag varchar(255) NOT NULL,
    data text NOT NULL,
    alter_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    master_id varchar(255) NOT NULL
);

CREATE INDEX idx_salt_events_tag on salt_events (tag);

EOF
```

Salt master configuration example:

```yaml
event_return: [postgres]
master_job_cache: postgres 
returner.postgres.host: 'db'
returner.postgres.user: 'alcali'
returner.postgres.passwd: 'alcali'
returner.postgres.db: 'salt'
returner.postgres.port: 5432
``` 

</p>
</details>

By default, jobs are only kept for 24 hours. Set `keep_jobs: 0` to disable the cache cleaner (see [managing the job cache](https://docs.saltstack.com/en/latest/topics/jobs/job_cache.html#managing-the-job-cache)).

Returners provide a way to archive old jobs. Refer to Salt [MySQL](https://docs.saltstack.com/en/latest/ref/returners/all/salt.returners.mysql.html#module-salt.returners.mysql) or [Postgres](https://docs.saltstack.com/en/latest/ref/returners/all/salt.returners.postgres.html) returner documentation for more information.

### Salt Api

Salt master configuration example:

```yaml
rest_cherrypy:
  port: 8080
  host: 0.0.0.0
  debug: True
  ssl_crt: /etc/pki/tls/certs/localhost.crt
  ssl_key: /etc/pki/tls/certs/localhost.key
```

Install instruction example (On Debian 9 using Salt python3 version):

```bash
apt-get install -y salt-api python3-openssl
salt-call --local tls.create_self_signed_cert cacert_path='/etc/pki'
```

Please refer to Salt [rest_cherrypy](https://docs.saltstack.com/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html#a-rest-api-for-salt) documentation for more infos on how to setup the salt-api.

### Authentication

Alcali provide a simple token based auth module for Salt.

You can get the Alcali auth module [here](https://raw.githubusercontent.com/latenighttales/alcali/2019.2.0/docker/saltconfig/salt/auth/alcali.py)

Place it on the salt filesystem (for example: `/srv/salt/auth`) and add it to your Salt master configuration:

```yaml
auth_dirs: [/srv/salt/auth]
```

Tokens can be managed using the [alcali](running.md) command or directly in the [web interface](views/users.md).

## Installing Alcali

!!!info
    Alcali follow Salt major and minor versioning.
    
    If you are using `2019.2.0` Salt version, you should install `2019.2.X` Alcali version.
 
There are 3 different ways to install Alcali:

 - Using a docker container
 - From PyPI
 - From Sources
 
#### Using Docker

The official [Docker image]() for Alcali comes with all dependencies pre-installed and ready-to-use with the latest version published on PyPI. Pull it with:

```commandline
docker pull latenighttales/alcali:2019.2.0
```
The `alcali` executable is provided as an entrypoint.

### Locally

To install Alcali locally, you'll need to install database connectors dependencies:

For Debian based distribution:
```commandline
apt install postgresql-dev
```
For Red-Hat based distribution:
```commandline
yum install postgresql-devel
```

#### Using pip

!!!warning

    We strongly recommend installing Alcali in a [virtualenv](https://docs.python.org/3/library/venv.html).
    
    Example:
    
    `python3 -m venv $HOME/.venv`
    
    `source $HOME/.venv/bin/activate`
    
Simply do:

```commandline
pip install 'alcali>=2019.2.0,2019.3.0'
```

#### From Sources

```commandline
git clone https://github.com/latenighttales/alcali.git
git checkout 2019.2.0
pip install .
```

## Troubleshooting
