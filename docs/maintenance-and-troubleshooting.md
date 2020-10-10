# Maintenance and Troubleshooting

## How to see the current status of your services

You can check the status of your services by using `systemctl status`. Example:
```
sudo systemctl status matrix-nginx-proxy

● matrix-nginx-proxy.service - Matrix nginx proxy server
   Loaded: loaded (/etc/systemd/system/matrix-nginx-proxy.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2018-11-14 19:38:35 UTC; 49min ago
```

You can see the logs by using journalctl. Example:
```
sudo journalctl -fu matrix-synapse
```


## Increasing Synapse logging

Because the [Synapse](https://github.com/matrix-org/synapse) Matrix server is originally very chatty when it comes to logging, we intentionally reduce its [logging level](https://docs.python.org/3/library/logging.html#logging-levels) from `INFO` to `WARNING`.

If you'd like to debug an issue or [report a Synapse bug](https://github.com/matrix-org/synapse/issues/new/choose) to the developers, it'd be better if you temporarily increasing the logging level to `INFO`.

Example configuration (`inventory/host_vars/matrix.DOMAIN/vars.yml`):

```yaml
matrix_synapse_log_level: "INFO"
matrix_synapse_storage_sql_log_level: "INFO"
matrix_synapse_root_log_level: "INFO"
```

Re-run the playbook after making these configuration changes.

## Remove unused Docker data

You can free some disk space from Docker, see [docker system prune](https://docs.docker.com/engine/reference/commandline/system_prune/) for more information.
```bash
ansible-playbook -i inventory/hosts setup.yml --tags=run-docker-prune
```

## Postgres

See the dedicated [PostgreSQL Maintenance](maintenance-postgres.md) documentation page.

## Ma1sd

See the dedicated [Adjusting ma1sd Identity Server configuration](configuring-playbook-ma1sd.md) documentation page.
