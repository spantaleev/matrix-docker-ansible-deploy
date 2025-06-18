<!--
SPDX-FileCopyrightText: 2019 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Michael Haak
SPDX-FileCopyrightText: 2021 - 2023 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Migrating to new server

This documentation explains how to migrate your Matrix services (server, client, bridges, etc.) and data **from an old server to a new server**.

**Notes**:
- This migration guide is applicable if you migrate from one server to another server having the same CPU architecture (e.g. both servers being `amd64`).

  If you're trying to migrate between different architectures (e.g. `amd64` --> `arm64`), simply copying the complete `/matrix` directory is **not** possible as it would move the raw PostgreSQL data (`/matrix/postgres/data`) between different architectures. In this specific case, you can use the guide below as a reference, but you would also need to avoid syncing `/matrix/postgres/data` to the new host, and also dump the database on your current server and import it properly on the new server. See our [Backing up PostgreSQL](maintenance-postgres.md#backing-up-postgresql) docs for help with PostgreSQL backup/restore.
- If you have any questions about migration or encountered an issue during migration, do not hesitate to ask for help on [our Matrix room](https://matrix.to/#/%23matrix-docker-ansible-deploy:devture.com). You probably might want to prepare a temporary/sub account on another Matrix server in case it becomes impossible to use your server due to migration failure by any chance.

- You can't change the domain (specified in the `matrix_domain` variable) after the initial deployment.

## Lower DNS TTL

Prepare by lowering DNS TTL for your domains (`matrix.example.com`, etc.), so that DNS record changes would happen faster, leading to less downtime.

## Stop services on the old server completely

Before migrating, you need to stop all services on the old server and make sure they won't be starting again.

To do so, it is recommended to run the `systemctl` command on the server. Running the playbook's `stop` tag also stops the services, but just once; they will start again if you reboot the server.

Log in to the old server and run the command as `root` (or a user that can run it with `sudo`):

```sh
cd /etc/systemd/system/ && systemctl disable --now matrix*
```

## Copy data directory to the new server

After you've confirmed that all services were stopped, copy the `/matrix` directory from the old server to the new server. When copying, make sure to preserve ownership and permissions (use `cp -p` or `rsync -ar`)!

## Adjust DNS records

Make sure your DNS records are adjusted to point to the new server's IP address.

## Update `inventory/hosts` file

Having adjusted DNS records, replace the old server's external IP address on the `inventory/hosts` file with that of the new server.

## Create `matrix` user and group on the new server

Then, run the command below on your local computer to create the `matrix` user and group on the new server:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-system-user
```

The shortcut command with `just` program is also available: `just run-tags setup-system-user`

**Note**: because the `matrix` user and group are created dynamically on each server, the user/group ID may differ between the old and new server. We suggest that you adjust ownership of `/matrix` files. To adjust the ownership, log in to the new server and run the command:

```sh
chown -R matrix:matrix /matrix
```

## Install and start all services on the new server

Finally, run the command below on your local computer to finish the installation and start all services:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-all,start
```

The shortcut command with `just` program is also available: `just run-tags install-all,start`

### Check if services work

After starting the services, you probably might want to ensure that you've migrated things correctly and that services are running. For instructions, see: [check if services work](maintenance-and-troubleshooting.md#how-to-check-if-services-work)

Having make sure that both services and federation work as expected, you can safely shutdown the old server.
