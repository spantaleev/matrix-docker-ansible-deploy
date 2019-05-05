# Updating users passwords

If you are using the matrix-postgres container(default), you can do it via this Ansible playbook (make sure to edit the `<your-username>` and `<your-password>` part below):

	ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=<your-username> password=<your-password>' --tags=update-user-password

**Note**: `<your-username>` is just a plain username (like `john`), not your full `@<username>:<your-domain>` identifier.

**You can then log in with that user** via the riot-web service that this playbook has created for you at a URL like this: `https://riot.<domain>/`.

If you are NOT using the matrix-postgres container, you can generate the password hash by using the command-line after **SSH**-ing to your server (requires that [all services have been started](#starting-the-services)):

	docker exec -it matrix-synapse /usr/local/bin/hash_password -c /data/homeserver.yaml

and then connecting to the postgres server and executing:

	UPDATE users SET password_hash = '<password-hash>' WHERE name = '@someone:server.com'

where `<password-hash>` is the hash returned by the docker command above.
