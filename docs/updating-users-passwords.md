# Updating users passwords

## Option 1

Use the Synapse User Admin API as described here: https://github.com/matrix-org/synapse/blob/master/docs/admin_api/user_admin_api.rst#reset-password

This requires an access token from a server admin account. If you didn't make your account a server admin when you created it, you can use the `/usr/local/bin/matrix-make-user-admin` script as described in [registering-users.md](registering-users.md).

## Option 2 (if you are using the default matrix-postgres container):

You can reset a user's password via the Ansible playbook (make sure to edit the `<your-username>` and `<your-password>` part below):

	ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=<your-username> password=<your-password>' --tags=update-user-password

**Note**: `<your-username>` is just a plain username (like `john`), not your full `@<username>:<your-domain>` identifier.

**You can then log in with that user** via the riot-web service that this playbook has created for you at a URL like this: `https://riot.<domain>/`.

## Option 3 (if you are using an external Postgres server):

You can manually generate the password hash by using the command-line after **SSH**-ing to your server (requires that [all services have been started](installing.md#starting-the-services)):

	docker exec -it matrix-synapse /usr/local/bin/hash_password -c /data/homeserver.yaml

and then connecting to the postgres server and executing:

	UPDATE users SET password_hash = '<password-hash>' WHERE name = '@someone:server.com'

where `<password-hash>` is the hash returned by the docker command above.
