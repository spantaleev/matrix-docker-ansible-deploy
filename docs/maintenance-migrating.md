> **Note**: This migration guide is applicable if you migrate from server to another that are of the same architecture, i.e. e.g. the servers both are amd64. 
> 
> In case that you migrate between two different architectures (e.g. amd64 --> arm64), simply copying the complete folder is not possible as it would move the raw PostgreSQL data between different architectures. In this specific case, you would need to dump the database on your current server and import it properly on the new server.
> 

# Migrating to new server

1. Prepare by lowering DNS TTL for your domains (`matrix.DOMAIN`, etc.), so that DNS record changes (step 4 below) would happen faster, leading to less downtime
2. Stop all services on the old server and make sure they won't be starting again. Execute this on the old server: `systemctl disable --now matrix*`
3. Copy directory `/matrix` from the old server to the new server. Make sure to preserve ownership and permissions (use `cp -p` or `rsync -ar`)!
4. Make sure your DNS records are adjusted to point to the new server's IP address
5. Remove old server from the `inventory/hosts` file and add new server.
6. Run `ansible-playbook -i inventory/hosts setup.yml --tags=setup-system-user`. This will create the `matrix` user and group on the new server
7. Because the `matrix` user and group are created dynamically on each server, the user/group id may differ between the old and new server. We suggest that you adjust ownership of `/matrix` files manually by running this on the new server: `chown -R matrix:matrix /matrix`.
8. Run `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start` to finish the installation and start all services
