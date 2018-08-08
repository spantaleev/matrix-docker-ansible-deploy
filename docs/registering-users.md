# Registering users

Run this to create a new user account on your Matrix server.

You can do it via this Ansible playbook (make sure to edit the `<your-username>` and `<your-password>` part below):

	ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=<your-username> password=<your-password> admin=<yes|no>' --tags=register-user

**or** using the command-line after **SSH**-ing to your server (requires that [all services have been started](#starting-the-services)):

	/usr/local/bin/matrix-synapse-register-user <your-username> <your-password> <admin access: 0 or 1>

**Note**: `<your-username>` is just a plain username (like `john`), not your full `@<username>:<your-domain>` identifier.