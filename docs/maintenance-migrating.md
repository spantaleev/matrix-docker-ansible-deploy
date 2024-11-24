# Migrating to new server

This documentation explains how to migrate your Matrix services (server, client, bridges, etc.) and data from an old server to a new server.

**Notes**:
- This migration guide is applicable if you migrate from one server to another server having the same CPU architecture (e.g. both servers being `amd64`).

  If you're trying to migrate between different architectures (e.g. `amd64` --> `arm64`), simply copying the complete `/matrix` directory is **not** possible as it would move the raw PostgreSQL data (`/matrix/postgres/data`) between different architectures. In this specific case, you can use the guide below as a reference, but you would also need to avoid syncing `/matrix/postgres/data` to the new host, and also dump the database on your current server and import it properly on the new server. See our [Backing up PostgreSQL](maintenance-postgres.md#backing-up-postgresql) docs for help with PostgreSQL backup/restore.
- If you have any questions about migration or encountered an issue during migration, do not hesitate to ask for help on [our Matrix room](https://matrix.to/#/%23matrix-docker-ansible-deploy:devture.com).

## Lower DNS TTL

Prepare by lowering DNS TTL for your domains (`matrix.example.com`, etc.), so that DNS record changes would happen faster, leading to less downtime.

## Stop services on the old server

Before migrating, you need to stop all services on the old server and make sure they won't be starting again.

To stop the services, go to the `matrix-docker-ansible-deploy` directory on your local computer, and run the command:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=stop
```

Alternatively, you can log in to the old server and run the command (you might have to `cd` to `/etc/systemd/system/` first):

```sh
systemctl disable --now matrix*
```

## Copy data directory to the new server

Then, copy directory `/matrix` from the old server to the new server. When copying, make sure to preserve ownership and permissions (use `cp -p` or `rsync -ar`)!

## Adjust DNS records

Make sure your DNS records are adjusted to point to the new server's IP address.

## Update `inventory/hosts` file

Having adjusted DNS records, replace the old server's external IP address on the `inventory/hosts` file with that of the new server.

**Note**: you can't change the domain after the initial deployment.

## Create `matrix` user and group on the new server

After updating `inventory/hosts` file, run the command below on your local computer to create the `matrix` user and group on the new server:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-system-user
```

**Note**: because the `matrix` user and group are created dynamically on each server, the user/group ID may differ between the old and new server. We suggest that you adjust ownership of `/matrix` files. To adjust the ownership, log in to the new server and run the command:

```sh
chown -R matrix:matrix /matrix
```

## Start all services on the new server

Finally, run the command below on your local computer to finish the installation and start all services:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-all,start
```

### Checking if services work

After starting the services, you can ensure that you've migrated things correctly and that services are running. For details, see: [check if services work](maintenance-checking-services.md)

Having make sure that both services and federation work as expected, you can safely shutdown the old server.
