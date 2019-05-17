# Try it!

If you just want to have a look, just clone the [repository](https://github.com/latenighttales/alcali.git) and use [docker-compose](https://docs.docker.com/compose/):

```commandline
git clone https://github.com/latenighttales/alcali.git
cd alcali
docker-compose -c docker-compose.demo.yml --scale minion=2
```

Once you see minions getting rejected by the master, you're good to go.

Just connect on [http://127.0.0.1:8000](http://127.0.0.1:8000), login with:

```commandline
username: admin
password: password
```

and follow the [walkthrough](walkthrough.md).