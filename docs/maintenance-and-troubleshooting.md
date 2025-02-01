# Maintenance and Troubleshooting

## How to see the current status of your services

You can check the status of your services by using `systemctl status`. Example:

```sh
sudo systemctl status matrix-synapse

● matrix-synapse.service - Synapse server
     Loaded: loaded (/etc/systemd/system/matrix-synapse.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2024-01-14 09:13:06 UTC; 1h 31min ago
```

## How to see the logs

Docker containers that the playbook configures are supervised by [systemd](https://wiki.archlinux.org/title/Systemd) and their logs are configured to go to [systemd-journald](https://wiki.archlinux.org/title/Systemd/Journal).

For example, you can find the logs of `matrix-synapse` in `systemd-journald` by logging in to the server with SSH and running the command as below:

```sh
sudo journalctl -fu matrix-synapse
```

Available service names can be seen by doing `ls /etc/systemd/system/matrix*.service` on the server. Some services also log to files in `/matrix/*/data/..`, but we're slowly moving away from that.

We just simply delegate logging to journald and it takes care of persistence and expiring old data.

### Enable systemd/journald logs persistence

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

## How to check if services work

The playbook can perform a check to ensure that you've configured things correctly and that services are running.

To perform the check, run:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=self-check
```

The shortcut command with `just` program is also available: `just run-tags self-check`

If it's all green, everything is probably running correctly.

Besides this self-check, you can also check whether your server federates with the Matrix network by using the [Federation Tester](https://federationtester.matrix.org/) against your base domain (`example.com`), not the `matrix.example.com` subdomain.

## Remove unused Docker data

You can free some disk space from Docker by removing its unused data. See [docker system prune](https://docs.docker.com/engine/reference/commandline/system_prune/) for more information.

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=run-docker-prune
```

The shortcut command with `just` program is also available: `just run-tags run-docker-prune`

## Postgres

See the dedicated [PostgreSQL Maintenance](maintenance-postgres.md) documentation page.
