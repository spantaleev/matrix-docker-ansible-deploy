# Uninstalling

**Warnings**:

- If your server federates with others, make sure to **leave any federated rooms before nuking your Matrix server's data**. Otherwise, the next time you set up a Matrix server for this domain (regardless of the installation method you use), you'll encounter trouble federating.

- If you have some trouble with your installation, you can just [re-run the playbook](installing.md) and it will try to set things up again. **Uninstalling and then installing anew rarely solves anything**.


-----------------


## Uninstalling using a script

Installing places a `/usr/local/bin/matrix-remove-all` script on the server.

You can run it to to have it uninstall things for you automatically (see below). **Use with caution!**


## Uninstalling manually

If you prefer to uninstall manually, run these commands (most are meant to be executed on the Matrix server itself):

- ensure all Matrix services are stopped: `ansible-playbook -i inventory/hosts setup.yml --tags=stop` (if you can't get Ansible working to run this command, you can run `systemctl stop 'matrix*'` manually on the server)

- delete the Matrix-related systemd `.service` and `.timer` files (`rm -f /etc/systemd/system/matrix*.{service,timer}`) and reload systemd (`systemctl daemon-reload`)

- delete some helper scripts (`rm -f /usr/local/bin/matrix*`)

- delete some cached Docker images (`docker system prune -a`) or just delete them all (`docker rmi $(docker images -aq)`)

- delete the Docker networks: `docker network rm matrix matrix-coturn` (might have been deleted already if you ran the `docker system prune` command)

- uninstall Docker itself, if necessary

- delete the `/matrix` directory (`rm -rf /matrix`)


