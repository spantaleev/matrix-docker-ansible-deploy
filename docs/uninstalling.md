# Uninstalling

**Note**: If you have some trouble with your installation configuration, you can just [re-run the playbook](installing.md) and it will try to set things up again. You don't need to uninstall and install fresh.

However, if you've installed this on some server where you have other stuff you wish to preserve, and now want get rid of Matrix, it's enough to do these:

- ensure all Matrix services are stopped (`systemctl stop 'matrix*'`)

- delete the Matrix-related systemd .service files (`rm -f /etc/systemd/system/matrix*`) and reload systemd (`systemctl daemon-reload`)

- delete all Matrix-related cronjobs (`rm -f /etc/cron.d/matrix*`)

- delete some helper scripts (`rm -f /usr/local/bin/matrix*`)

- delete some cached Docker images (or just delete them all: `docker rmi $(docker images -aq)`)

- delete the Docker network: `docker network rm matrix`

- uninstall Docker itself, if necessary

- delete the `/matrix` directory (`rm -rf /matrix`)

The script `/usr/local/bin/matrix-remove-all` performs all these steps (**use with caution!**).

