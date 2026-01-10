<!--
SPDX-FileCopyrightText: 2018 Aaron Raimist
SPDX-FileCopyrightText: 2019 - 2020 MDAD project contributors
SPDX-FileCopyrightText: 2019 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Noah Fleischmann
SPDX-FileCopyrightText: 2020 Marcel Partap
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Maintenance and Troubleshooting

## Maintenance

### How to back up the data on your server

We haven't documented this properly yet, but the general advice is to:

- back up Postgres by making a database dump. See [Backing up PostgreSQL](maintenance-postgres.md#backing-up-postgresql)

- back up all `/matrix` files, except for `/matrix/postgres/data` (you already have a dump) and `/matrix/postgres/data-auto-upgrade-backup` (this directory may exist and contain your old data if you've [performed a major Postgres upgrade](maintenance-postgres.md#upgrading-postgresql)).

You can later restore these by:

- Restoring the `/matrix` directory and files on the new server manually
- Following the instruction described on [Installing a server into which you'll import old data](installing.md#installing-a-server-into-which-youll-import-old-data)

If your server's IP address has changed, you may need to [set up DNS](configuring-dns.md) again.

### Remove unused Docker data

You can free some disk space from Docker by removing its unused data. See [docker system prune](https://docs.docker.com/engine/reference/commandline/system_prune/) for more information.

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=run-docker-prune
```

The shortcut command with `just` program is also available: `just run-tags run-docker-prune`

### Postgres

See the dedicated [PostgreSQL maintenance](maintenance-postgres.md) documentation page.

### Synapse

See the dedicated [Synapse maintenance](maintenance-synapse.md) documentation page.

## Troubleshooting

### How to see the current status of your services

You can check the status of your services by using `systemctl status`. Example:

```sh
sudo systemctl status matrix-synapse

● matrix-synapse.service - Synapse server
     Loaded: loaded (/etc/systemd/system/matrix-synapse.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2024-01-14 09:13:06 UTC; 1h 31min ago
```

### How to see the logs

Docker containers that the playbook configures are supervised by [systemd](https://wiki.archlinux.org/title/Systemd) and their logs are configured to go to [systemd-journald](https://wiki.archlinux.org/title/Systemd/Journal).

For example, you can find the logs of `matrix-synapse` in `systemd-journald` by logging in to the server with SSH and running the command as below:

```sh
sudo journalctl -fu matrix-synapse
```

Available service names can be seen by doing `ls /etc/systemd/system/matrix*.service` on the server. Some services also log to files in `/matrix/*/data/..`, but we're slowly moving away from that.

We just simply delegate logging to journald and it takes care of persistence and expiring old data.

#### Enable systemd/journald logs persistence

On some distros, the journald logs are just in-memory and not persisted to disk.

Consult (and feel free to adjust) your distro's journald logging configuration in `/etc/systemd/journald.conf`.

To enable persistence and put some limits on how large the journal log files can become, adjust your configuration like this:

```ini
[Journal]
RuntimeMaxUse=200M
SystemMaxUse=1G
RateLimitInterval=0
RateLimitBurst=0
Storage=persistent
```

### How to check if services work

The playbook can perform a check to ensure that you've configured things correctly and that services are running.

To perform the check, run:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=self-check
```

The shortcut command with `just` program is also available: `just run-tags self-check`

If it's all green, everything is probably running correctly.

Besides this self-check, you can also check whether your server federates with the Matrix network by using the [Federation Tester](https://federationtester.matrix.org/) against your base domain (`example.com`), not the `matrix.example.com` subdomain.

### How to debug or force SSL certificate renewal

SSL certificates are managed automatically by the [Traefik](https://doc.traefik.io/traefik/) reverse-proxy server.

If you're having trouble with SSL certificate renewal, check the Traefik logs (`journalctl -fu matrix-traefik`).

If you're [using your own webserver](configuring-playbook-own-webserver.md) instead of the integrated one (Traefik), you should investigate in another way.
