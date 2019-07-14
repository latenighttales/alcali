# Alcali

[![Build Status](https://travis-ci.org/latenighttales/alcali.svg?branch=2019.2.0)](https://travis-ci.org/latenighttales/alcali)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=latenighttales/alcali)](https://dependabot.com)
[![codecov](https://codecov.io/gh/latenighttales/alcali/branch/2019.2.0/graph/badge.svg)](https://codecov.io/gh/latenighttales/alcali)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

<img align="right" height="300" src="https://upload.wikimedia.org/wikipedia/commons/5/5f/Logo_du_Mois_de_la_contribution_sans_texte.svg">


## What's Alcali?

Alcali is a web based tool for monitoring and administrating **Saltstack** Salt.

## Features

- Get notified in real time when a job is created, updated or has returned. 

- Store your jobs results by leveraging the `master_job_store` setting with Alcali master returner.

- Check your minions conformity to their highstate.

- Keep track of custom state at a glance.

- Use custom auth module to login into both Alcali and the Salt-api using JWT.

## Try it!

If you just want to have a look, just clone the [repository](https://github.com/latenighttales/alcali.git) and use [docker-compose](https://docs.docker.com/compose/):

```bash
git clone https://github.com/latenighttales/alcali.git
cd alcali
docker-compose up --scale minion=2
```


Once you see minions waiting to be approved by the master, you're good to go:

```bash
...
minion_1  | [ERROR   ] The Salt Master has cached the public key for this node, this salt minion will wait for 10 seconds before attempting to re-authenticate
minion_1  | [INFO    ] Waiting 10 seconds before retry.
...
```

Just connect on [http://127.0.0.1:8000](http://127.0.0.1:8000), login with:

```commandline
username: admin
password: password
```

and follow the [walkthrough](https://alcali.dev/walkthrough/).

Once you're done, you can [install it](https://alcali.dev/installation/).
## Licence

[MIT](LICENSE)

## Contributing

If you'd like to contribute, simply fork the repository, commit your changes, run the tests and send a pull request.

<sub><sub>Image: Jean-Philippe WMFr, derivative work : User:Benoit Rochon [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0)</sub></sub>
