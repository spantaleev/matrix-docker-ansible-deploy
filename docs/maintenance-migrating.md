# Migrating to new server

1. Backup directory `/matrix`. Make sure to preserve owner and permission (use `cp -p`)!
2. Remove old server from matrix-docker-ansible-deploy `hosts` file and add new server.
3. Run `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all`. This will create the matrix user and group.
4. Copy backup from old server to new server. Make sure to preserve owner and permission (use `cp -p`)!
5. Run `ansible-playbook -i inventory/hosts setup.yml --tags=start`
