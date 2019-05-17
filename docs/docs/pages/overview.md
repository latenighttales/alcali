# Overview

(screenshot of overview)

## Conformity

Conformity settings can be managed on the [conformity](conformity.md) page.

You can set a maximum of 4 custom conformity fields. To be relevant, functions tracked by conformity fields must be run regularly.


## Keys

Summary of keys status.

You can manage keys on the [keys](keys.md) page.

## Status

#### SALT WEB SOCKET

To display notifications on currently running jobs, alcali needs to connect to the Salt master web socket using credentials provided in the [configuration](../configuration.md).

#### JOBS AND EVENTS IN DB

Please refer to [Mysql](https://docs.saltstack.com/en/latest/ref/returners/all/salt.returners.mysql.html) or [Postgres](https://docs.saltstack.com/en/latest/ref/returners/all/salt.returners.postgres.html) returner documentation on how to manage database from Salt. A summary is provided in the [installation](../installation.md) section.

#### JOBS SCHEDULED

How many unique jobs based on the job name are currently enabled (see [schedule](schedule.md) section).

#### JOBS RUNNING

Parsed from Salt web socket.

## Jobs Stats

Filter:

 - ALL: All jobs.
 - HIGHSTATE: only `state.apply` and `state.highstate` jobs.
 - OTHER: All excluding `state.apply` and `state.highstate` jobs.
 
## Last Jobs

The last 10 jobs run (see [jobs](jobs.md) section).

## Real time events

JSON Formatted Events.