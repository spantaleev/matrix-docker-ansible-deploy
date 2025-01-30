# Maintenance and Troubleshooting

## How to see the current status of your services

You can check the status of your services by using `systemctl status`. Example:

```sh
sudo systemctl status matrix-synapse

● matrix-synapse.service - Synapse server
     Loaded: loaded (/etc/systemd/system/matrix-synapse.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2024-01-14 09:13:06 UTC; 1h 31min ago
```

Docker containers that the playbook configures are supervised by [systemd](https://wiki.archlinux.org/title/Systemd) and their logs are configured to go to [systemd-journald](https://wiki.archlinux.org/title/Systemd/Journal).

To prevent double-logging, Docker logging is disabled by explicitly passing `--log-driver=none` to all containers. Due to this, you **cannot** view logs using `docker logs`.

To view systemd-journald logs using [journalctl](https://man.archlinux.org/man/journalctl.1), run a command like this:

```sh
sudo journalctl -fu matrix-synapse
```

## Increase logging verbosity

Because the [Synapse](https://github.com/element-hq/synapse) Matrix server is originally very chatty when it comes to logging, we intentionally reduce its [logging level](https://docs.python.org/3/library/logging.html#logging-levels) from `INFO` to `WARNING`.

If you'd like to debug an issue or [report a Synapse bug](https://github.com/element-hq/synapse/issues/new/choose) to the developers, it'd be better if you temporarily increasing the logging level to `INFO`.

Example configuration (`inventory/host_vars/matrix.example.com/vars.yml`):

```yaml
matrix_synapse_log_level: "INFO"
matrix_synapse_storage_sql_log_level: "INFO"
matrix_synapse_root_log_level: "INFO"
```

Re-run the playbook after making these configuration changes.

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

You can free some disk space from Docker, see [docker system prune](https://docs.docker.com/engine/reference/commandline/system_prune/) for more information.

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=run-docker-prune
```

The shortcut command with `just` program is also available: `just run-tags run-docker-prune`

## Postgres

See the dedicated [PostgreSQL Maintenance](maintenance-postgres.md) documentation page.
