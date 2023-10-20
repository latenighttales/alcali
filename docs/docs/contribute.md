# Contributing Guide

Contributing to Alcali is fairly easy. This document shows you how to get started

## General
Please ensure that any changes you make are in accordance with the Coding Guidelines of this repo.

Just use [Black](https://github.com/python/black) to validate your python code.

## Install a dev environment

First [fork](https://github.com/latenighttales/alcali/fork) the repository and install your fork locally.

```commandline
git clone git@github.com:<YOUR USERNAME>/alcali.git
cd alcali
```

Alcali use Vuejs for the frontend and Django for the backend.

### Frontend dev

Install the Vue CLI:

```commandline
npm install -g @vue/cli
# OR
yarn global add @vue/cli
```
install js deps:

```commandline
npm install
# OR
yarn install
```
and run your build locally:

```commandline
npm run serve -- --port 8001
```

You will also need a [backend](#backend-dev) running in another terminal.

### Backend dev

```commandline
docker compose up --build --force-recreate --renew-anon-volumes --scale minion=2
```

### Documentation

To contribute to the documentation, you'll need to install the python requirements, preferably in a virtualenv:

```commandline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/docs.txt
```
And build it locally:

```commandline
cd docs
mkdocs serve -a 127.0.0.1:8003
```

### Run tests locally

```commandline
docker compose -f docker-compose-ci.yml up --build 
```

and in another shell:

```commandline
./docker/utils/ci_script.sh
```
Tests are idempotent~ish


## Submitting changes

 Check out a new branch based and name it to what you intend to do:
````
$ git checkout -b BRANCH_NAME feature/fooBar
````
If you get an error, you may need to fetch fooBar first by using
````
$ git remote update && git fetch
````
Use one branch per fix / feature

Commit your changes

- Please provide a git message that explains what you've done
- Please make sure your commits follow the [conventions](https://gist.github.com/robertpainsi/b632364184e70900af4ab688decf6f53#file-commit-message-guidelines-md)
- Commit to the forked repository
````
$ git commit -am 'Add some fooBar'
````
Push to the branch
````
$ git push origin feature/fooBar
````
Make a pull request
- Make sure you send the PR to the <code>fooBar</code> branch
- Travis CI is watching you!

If you follow these instructions, your PR will land pretty safely in the main repo!