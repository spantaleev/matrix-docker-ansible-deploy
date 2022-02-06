# Updating users passwords

## Option 1 (if you are using the default matrix-postgres container):

You can reset a user's password via the Ansible playbook (make sure to edit the `<your-username>` and `<your-password>` part below):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=<your-username> password=<your-password>' --tags=update-user-password
```

**Note**: `<your-username>` is just a plain username (like `john`), not your full `@<username>:<your-domain>` identifier.

**You can then log in with that user** via the Element service that this playbook has created for you at a URL like this: `https://element.<domain>/`.


## Option 2 (if you are using an external Postgres server):

You can manually generate the password hash by using the command-line after **SSH**-ing to your server (requires that [all services have been started](installing.md#starting-the-services)):

```
docker exec -it matrix-synapse /usr/local/bin/hash_password -c /data/homeserver.yaml
```

and then connecting to the postgres server and executing:

```
UPDATE users SET password_hash = '<password-hash>' WHERE name = '@someone:server.com'
```

where `<password-hash>` is the hash returned by the docker command above.


## Option 3:

Use the Synapse User Admin API as described here: https://github.com/matrix-org/synapse/blob/master/docs/admin_api/user_admin_api.rst#reset-password

This requires an access token from a server admin account. *This method will also log the user out of all of their clients while the other options do not.*

If you didn't make your account a server admin when you created it, you can use the `/usr/local/bin/matrix-change-user-admin-status` script as described in [registering-users.md](registering-users.md).

### Example:
To set @user:domain.com's password to `correct_horse_battery_staple` you could use this curl command:
```
curl -XPOST -d '{ "new_password": "correct_horse_battery_staple" }' "https://matrix.<domain>/_matrix/client/r0/admin/reset_password/@user:domain.com?access_token=MDA...this_is_my_access_token
```
