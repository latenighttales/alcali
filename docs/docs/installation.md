# Installation

## Prerequisite

Alcali try to be **very** modular.

The minimal requirement is a database (**MariaDB/Mysql** or **Postgres**) accessible to both your Salt master and Alcali and the [Salt-Api](https://docs.saltstack.com/en/latest/ref/cli/salt-api.html#salt-api) accessible.

![structure](images/structure.png)

 

## Preparing the salt master

### Database access and master job store configuration

Please refer to Salt [MySQL](https://docs.saltstack.com/en/latest/ref/returners/all/salt.returners.mysql.html#module-salt.returners.mysql) or [Postgres](https://docs.saltstack.com/en/latest/ref/returners/all/salt.returners.pgjsonb.html) returner documentation. It provide both the database schema and the needed master configuration.

Here is a Salt master configuration example:

```yaml
event_return: [mysql]
master_job_cache: mysql
mysql.host: 'db'
mysql.user: 'alcali'
mysql.pass: 'alcali'
mysql.db: 'salt'
mysql.port: 3306
``` 

Returners provide a way to archive old jobs.

!!!warning
    
    Don't forget to install database connectors:
    
     - `python-mysqldb` for MySQL/MariaDB
     - `python-psycopg2` for Postgres
     
### Formula

You can find a Salt formula to manage salt master configuration [here]()

### Salt Api

Please refer to Salt [rest_cherrypy](https://docs.saltstack.com/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html#a-rest-api-for-salt) documentation on how to setup the salt-api.

## Installing Alcali

There is 3 different ways to run Alcali:

 - Using a docker container
 - From PyPI
 - From Source
 
!!!info
    Alcali follow Salt major and minor versioning.
    
    If you are using `2019.2.0` Salt version, you should install `2019.2.X` Alcali version.
 
#### Using Docker

The official [Docker image]() for Alcali comes with all dependencies pre-installed and ready-to-use with the latest version published on PyPI. Pull it with:

```commandline
docker pull latenighttales/alcali:2019.2.0
```
The `alcali` executable is provided as an entrypoint.


#### Using pip

!!!info

    We strongly recommend installing in a [virtualenv](https://docs.python.org/3/library/venv.html).
    
Simply do:
```commandline
pip install 'alcali>=2019.2.0,2019.3.0'
```

#### From Github

```commandline
git clone https://github.com/latenighttales/alcali.git
pip install .
```

### Troubleshooting
