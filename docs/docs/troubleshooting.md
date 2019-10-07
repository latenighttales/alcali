# Troubleshooting

## Salt-Api connection

you can try [this](https://docs.saltstack.com/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html#authentication) `curl` command using pam authentication and see if you can login

## Salt-Api using the alcali auth module

If the salt-api works with pam auth, then there's probably an issue with the [alcali authentication](installation.md#authentication):

- Is the auth module accessible to salt? (it should be in a sub folder called `auth` of the [file_roots](https://docs.saltstack.com/en/latest/ref/file_server/file_roots.html#directory-overlay)
- Have you run `salt-run saltutil.sync_all` on the salt-master? it is needed for the salt-master to "see" the auth module.

Log messages of the salt-api and salt-master should tell you if the module is found and auth is successful.

## Salt Master configuration example

A salt-master configuration in the [repository](https://github.com/latenighttales/alcali/blob/2019.2/docker/saltconfig/etc/master) as an example.

