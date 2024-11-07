# Updating users passwords

## Option 1 (if you are using the integrated Postgres database):

You can reset a user's password via the Ansible playbook (make sure to edit the `<your-username>` and `<your-password>` part below):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=<your-username> password=<your-password>' --tags=update-user-password
```

**Note**: `<your-username>` is just a plain username (like `john`), not your full `@<username>:example.com` identifier.

**You can then log in with that user** via Element Web that this playbook has created for you at a URL like this: `https://element.example.com/`.


## Option 2 (if you are using an external Postgres server):

You can manually generate the password hash by using the command-line after **SSH**-ing to your server (requires that [all services have been started](installing.md#starting-the-services)):

```
docker exec -it matrix-synapse /usr/local/bin/hash_password -c /data/homeserver.yaml
```

and then connecting to the postgres server and executing:

```sql
UPDATE users SET password_hash = '<password-hash>' WHERE name = '@someone:example.com';
```

where `<password-hash>` is the hash returned by the docker command above.


## Option 3:

Use the Synapse User Admin API as described here: https://github.com/element-hq/synapse/blob/master/docs/admin_api/user_admin_api.rst#reset-password

This requires an [access token](obtaining-access-tokens.md) from a server admin account. *This method will also log the user out of all of their clients while the other options do not.*

If you didn't make your account a server admin when you created it, you can learn how to switch it now by reading about it in [Adding/Removing Administrator privileges to an existing Synapse user](registering-users.md#addingremoving-administrator-privileges-to-an-existing-synapse-user).

### Example:
To set @user:example.com's password to `correct_horse_battery_staple` you could use this curl command:
```
curl -XPOST -d '{ "new_password": "correct_horse_battery_staple" }' "https://matrix.example.com/_matrix/client/r0/admin/reset_password/@user:example.com?access_token=MDA...this_is_my_access_token
```
