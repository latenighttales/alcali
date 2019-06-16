# Try it!

If you just want to have a look, just clone the [repository](https://github.com/latenighttales/alcali.git) and use [docker-compose](https://docs.docker.com/compose/):

```commandline
git clone https://github.com/latenighttales/alcali.git
cd alcali
docker-compose up --scale minion=2
```


Once you see minions waiting to be approved by the master, you're good to go:

```commandline
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

and follow the [walkthrough](walkthrough.md).

Once you're done, you can [install it](installation.md).